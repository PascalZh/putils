import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider
from matplotlib import rcParams


class SliderParam(object):
    def __init__(self, label, valmin, valmax, valinit, **slider_kwargs) -> None:
        self.label = label
        self.valmin = valmin
        self.valmax = valmax
        self.valinit = valinit
        self.slider_kwargs = slider_kwargs


class PlotUI(object):
    def __init__(self, *fig_args, **fig_kwargs) -> None:
        self.fig = plt.figure(*fig_args, **fig_kwargs)


class PlotUI_Sliders(PlotUI):
    def __init__(self, num_plots, params_bottom: tuple, params_right: tuple, styles=None, *fig_args, **fig_kwargs) -> None:
        """UI with up to 4 plots and bottom/right sliders and a reset button.

        Args:
            num_plots: can be 1, 2, 3, 4
            params_bottom: a tuple of :obj:SliderParam for bottom sliders, (name, val_min, val_max, val_init)
            params_right: see `params_bottom`
            styles (optional): pass None to use default styles. Defaults to None.

        """
        super().__init__(*fig_args, **fig_kwargs)
        self.styles = {
            'facecolor': 'lightgoldenrodyellow'} if styles is None else styles

        self.fig.subplots_adjust(bottom=rcParams['figure.subplot.bottom']+0.05*len(params_bottom),
                                 right=rcParams['figure.subplot.right']-0.065*len(params_right))

        self.axes = []
        'row major indexed lists of axes'
        if num_plots == 1:
            self.axes.append(self.fig.add_subplot(111))
        elif num_plots == 2:
            self.axes.append(self.fig.add_subplot(211))
            self.axes.append(self.fig.add_subplot(212))
        elif num_plots == 3:
            self.axes.append(self.fig.add_subplot(221))
            self.axes.append(self.fig.add_subplot(222))
            self.axes.append(self.fig.add_subplot(223))
        elif num_plots == 4:
            self.axes.append(self.fig.add_subplot(221))
            self.axes.append(self.fig.add_subplot(222))
            self.axes.append(self.fig.add_subplot(223))
            self.axes.append(self.fig.add_subplot(224))
        else:
            raise RuntimeError("num_plots should be between 1 and 4")

        self.params_bottom = params_bottom
        self.params_right = params_right
        self.axes_bottom, self.sliders_bottom = self._init_sliders(
            params_bottom, orientation='horizontal')
        self.axes_right, self.sliders_right = self._init_sliders(
            params_right, orientation='vertical')

        self.ax_button, self.button_reset = self._init_button_reset()

    @property
    def sliders(self):
        return self.sliders_bottom + self.sliders_right

    def _init_sliders(self, params, orientation):
        facecolor = self.styles['facecolor']
        ret = [], []
        left = self.fig.subplotpars.left
        right = self.fig.subplotpars.right
        bottom = self.fig.subplotpars.bottom
        top = self.fig.subplotpars.top

        for i, param in enumerate(params):
            if orientation == 'horizontal':
                width_offset = 0.12 if len(self.params_right) <= 1 else 0.0
                ret[0].append(
                    plt.axes([left, 0.05+0.05*i, right-left-width_offset, 0.03], facecolor=facecolor))
            else:
                ret[0].append(
                    plt.axes([right+0.08+0.065*i, bottom, 0.03, top-bottom], facecolor=facecolor))
            ret[1].append(Slider(
                ret[0][-1],
                param.label,
                param.valmin,
                param.valmax,
                valinit=param.valinit,
                color='green',
                orientation=orientation,
                **param.slider_kwargs
            ))
        return ret

    def _init_button_reset(self):
        ax = plt.axes([0.86, 0.05, 0.09, 0.03])
        color = self.styles['facecolor']
        button = Button(
            ax, 'Reset', color=color, hovercolor='0.975')

        def reset(event):
            for slider in self.sliders:
                slider.reset()
        button.on_clicked(reset)
        return ax, button

    def on_changed(self, update):
        for slider in self.sliders:
            slider.on_changed(update)
