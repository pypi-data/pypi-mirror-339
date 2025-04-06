from typing import Dict, Optional, Union, List, Tuple
import pandas as pd
import numpy as np
from matplotlib.axes import Axes

from quickstats.plots import get_color_cycle, get_cmap

from quickstats.plots import AbstractPlot, StatPlotConfig
from quickstats.plots.core import get_rgba
from quickstats.plots.template import create_transform, handle_has_label
from quickstats.utils.common_utils import combine_dict
from .core import ErrorDisplayFormat

class TwoPanel1DPlot(AbstractPlot):

    STYLES = {
        'fill_between': {
             'alpha': 0.3,
             'hatch': None,
             'linewidth': 1.0
        },
        'ratio_frame':{
            'height_ratios': (1, 1),
            'hspace': 0.05           
        },
        'legend_lower': {
        }
    }

    CONFIG: Dict[str, bool] = {
        'error_format': 'fill',
        'isolate_error_legend': False,
        'inherit_color': True,
        'error_on_top': True
    }    
    
    def __init__(self, data_map:Union[pd.DataFrame, Dict[str, pd.DataFrame]],
                 label_map:Optional[Dict]=None,
                 styles_map:Optional[Dict]=None,
                 color_cycle=None,
                 color_cycle_lower=None,
                 styles:Optional[Union[Dict, str]]=None,
                 analysis_label_options:Optional[Dict]=None,
                 config:Optional[Dict]=None):
        
        self.data_map = data_map
        
        super().__init__(color_cycle=color_cycle,
                         label_map=label_map,
                         styles_map=styles_map,
                         styles=styles,
                         analysis_label_options=analysis_label_options,
                         config=config)
        if color_cycle_lower is not None:
            self.cmap_lower = get_cmap(color_cycle_lower)
        else:
            self.cmap_lower = None
        
    def get_default_legend_order(self):
        if not isinstance(self.data_map, dict):
            return []
        else:
            return list(self.data_map)
        
    def draw_single_data(self, ax, data:pd.DataFrame,
                         xattrib:str, yattrib:str,
                         yerrloattrib:Optional[str]=None,
                         yerrhiattrib:Optional[str]=None,
                         stat_configs:Optional[List[StatPlotConfig]]=None,
                         styles:Optional[Dict]=None,
                         label:Optional[str]=None):
        data = data.reset_index()
        x, y = data[xattrib].values, data[yattrib].values
        indices = np.argsort(x)
        x, y = x[indices], y[indices]
        draw_styles = combine_dict(self.styles['plot'], styles)
        fill_styles = combine_dict(self.styles['fill_between'])
            
        if (yerrloattrib is not None) and (yerrhiattrib is not None):
            yerrlo = data[yerrloattrib][indices]
            yerrhi = data[yerrhiattrib][indices]
            handle_fill = ax.fill_between(x, yerrlo, yerrhi,
                                          **fill_styles)
        else:
            handle_fill = None
        
        handle_plot = ax.plot(x, y, **draw_styles, label=label)
        if isinstance(handle_plot, list) and (len(handle_plot) == 1):
            handle_plot = handle_plot[0]

        if handle_fill and ('color' not in fill_styles):
            plot_color = handle_plot.get_color()
            fill_color = get_rgba(plot_color)
            handle_fill.set_color(fill_color)

        if self.config['errorband_legend'] and (handle_fill is not None):
            handles = (handle_plot, handle_fill)
        else:
            handles = handle_plot
        return handles

    def get_target_data(
        self,
        target: Optional[str],
        xattrib: str,
        yattrib: str,
        yerrloattrib: Optional[str] = None,
        yerrhiattrib: Optional[str] = None,
    ):
        if target not in self.data_map:
            raise ValueError(f'Target dataset does not exist: {target}')
        data = self.data_map[target].reset_index()
        x, y = data[xattrib].values, data[yattrib].values
        indices = np.argsort(x)
        x, y = x[indices], y[indices]

        if ((yerrloattrib and yerrloattrib in data) and 
            (yerrhiattrib and yerrhiattrib in data)):
            yerrlo = data[yerrloattrib].values[indices]
            yerrhi = data[yerrhiattrib].values[indices]
            yerr = (yerrlo, yerrhi)
        else:
            yerr = None
        return x, y, yerr    

    def draw_single_target(
        self,
        ax: Axes,
        target: Optional[str],
        xattrib: str,
        yattrib: str,
        yerrloattrib: Optional[str] = None,
        yerrhiattrib: Optional[str] = None,
        offset_error: bool = False,
        domain: Optional[str]=None
    ):
        
        x, y, yerr = self.get_target_data(
            target,
            xattrib=xattrib,
            yattrib=yattrib,
            yerrloattrib=yerrloattrib,
            yerrhiattrib=yerrhiattrib,
        )
            
        handles: Dict[str, Any] = {}
        styles = self.get_target_styles('plot', target)
        styles['label'] = self.get_target_label(target, domain)  or target
        # need to extract the first entry since we are drawing 1D data
        handles[target], = ax.plot(x, y, **styles)

        if yerr is not None:
            error_format = self.get_target_config('error_format', target)
            error_format = ErrorDisplayFormat.parse(error_format)
            error_styles = self.get_target_styles(error_format.artist, target)

            inherit_color = self.get_target_config('inherit_color', target)
            if inherit_color:
                error_styles.setdefault('color', handles[target].get_color())

            error_target = self.label_map.format(target, 'error')
            error_styles['label'] = self.label_map.get(error_target) or error_target

            zorder = handles[target].get_zorder()
            error_on_top = self.get_target_config('error_on_top', target)
            error_styles['zorder'] = zorder + (0.1 if error_on_top else -0.1)

            if error_format == ErrorDisplayFormat.ERRORBAR:
                error_handle = ax.errorbar(x, y, yerr, **error_styles)
            elif error_format == ErrorDisplayFormat.FILL:
                if offset_error:
                    error_handle = ax.fill_between(x, y - yerr[0], y + yerr[1], **error_styles)
                else:
                    error_handle = ax.fill_between(x, yerr[0], yerr[1], **error_styles)
            else:
                raise RuntimeError(f'unsupported error format: {error_format.name}')

            isolate_error_legend = self.get_target_config('isolate_error_legend', target)
            if not isolate_error_legend:
                handles[target] = (handles[target], error_handle)
            else:
                handles[error_target] = error_handle
                
        self.update_legend_handles(handles, domain=domain)
        self.legend_order.extend(handles.keys())    
    
    def draw(
        self,
        xattrib:str,
        yattrib_upper:str,
        yattrib_lower:str,
        targets_upper:Optional[List[str]],
        targets_lower:Optional[List[str]],
        yerrloattrib_upper:Optional[str]=None,
        yerrhiattrib_upper:Optional[str]=None,
        yerrloattrib_lower:Optional[str]=None,
        yerrhiattrib_lower:Optional[str]=None,
        offset_error: bool = False,
        xlabel:Optional[str]=None,
        xmin:Optional[float]=None,
        xmax:Optional[float]=None,
        ylabel_upper:Optional[str]=None,
        ylabel_lower:Optional[str]=None,
        ymin_lower:Optional[float]=None,
        ymin_upper:Optional[float]=None,
        ymax_lower:Optional[float]=None,
        ymax_upper:Optional[float]=None,
        ypad_upper:Optional[float]=0.3,
        ypad_lower:Optional[float]=0.3,
        logx:bool=False,
        logy_upper:bool=False,
        logy_lower:bool=False,
        legend_order_upper: Optional[List[str]] = None,
        legend_order_lower: Optional[List[str]] = None
    ):

        if not isinstance(self.data_map, dict):
            raise ValueError('invalid data format')

        if self.cmap_lower is not None:
            prop_cycle_lower = get_color_cycle(self.cmap_lower)
        else:
            prop_cycle_lower = None
        ax_upper, ax_lower = self.draw_frame(logx=logx, logy=logy_upper,
                                             logy_lower=logy_lower,
                                             prop_cycle_lower=prop_cycle_lower,
                                             ratio=True)

        if self.styles_map is None:
            styles_map = {k:None for k in self.data_map}
        else:
            styles_map = self.styles_map
            
        if self.label_map is None:
            label_map = {k:k for k in self.data_map}
        else:
            label_map = self.label_map
            
        for (domain, ax, targets, yattrib,
             yerrloattrib, yerrhiattrib) in [
            ('upper', ax_upper, targets_upper, yattrib_upper, yerrloattrib_upper, yerrhiattrib_upper),
            ('lower', ax_lower, targets_lower, yattrib_lower, yerrloattrib_lower, yerrhiattrib_lower)
        ]:
            for target in targets:
                self.draw_single_target(
                    ax,
                    target=target,
                    xattrib=xattrib,
                    yattrib=yattrib,
                    yerrloattrib=yerrloattrib,
                    yerrhiattrib=yerrhiattrib,
                    offset_error=offset_error,
                    domain=domain
                )

        self.draw_axis_components(ax_upper, ylabel=ylabel_upper)
        ax_upper.tick_params(axis='x', labelbottom=False)
        self.draw_axis_components(ax_lower, xlabel=xlabel, ylabel=ylabel_lower)
        self.set_axis_range(ax_upper, xmin=xmin, xmax=xmax,
                            ymin=ymin_upper, ymax=ymax_upper, ypad=ypad_upper)
        self.set_axis_range(ax_lower, xmin=xmin, xmax=xmax,
                            ymin=ymin_lower, ymax=ymax_lower, ypad=ypad_lower)

        self.draw_legend(
            ax_upper,
            domains='upper',
            targets=legend_order_upper,
            **self.styles['legend']
        )
        self.draw_legend(
            ax_lower,
            domains='lower',
            targets=legend_order_lower,
            **self.styles['legend_lower']
        )
        return ax_upper, ax_lower
