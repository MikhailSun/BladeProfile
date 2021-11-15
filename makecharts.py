# -*- coding: utf-8 -*-
"""
Редактор Spyder

Это временный скриптовый файл.
TODO!!! добавить возможность вручную настраивать цену деления шкалы осей set_xticks или как-то так
"""

from matplotlib import pyplot as plt
import numpy as np

#вспомоагтельный класс для быстрого построения графиков
class Chart():
    
    def __init__(self,points_for_scatter=[],points_for_plot=[],title='',xlabel='',ylabel='',ylabel2='',xlim=np.nan,ylim=np.nan,y2lim=np.nan,fontsize='medium',color_ticklabels='black', color_fig='white', color_axes='white',figure_size=(10,6),dpi=100):
        self.left_margin=0.15
        self.bottom_margin=0.1
        self.margin_between_axes=0.05

        self.__add_chart(points_for_scatter=points_for_scatter,points_for_plot=points_for_plot,title=title,xlabel=xlabel,ylabel=ylabel,ylabel2=ylabel2,xlim=xlim,ylim=ylim,y2lim=y2lim,fontsize=fontsize,color_ticklabels=color_ticklabels, color_fig=color_fig, color_axes=color_axes,figure_size=figure_size,dpi=dpi)
    def add_chart(self,points_for_scatter=[],points_for_plot=[],title='',xlabel='',ylabel='',ylabel2='',xlim=np.nan,ylim=np.nan,y2lim=np.nan,fontsize='medium',color_ticklabels='black', color_fig='white', color_axes='white'):
        self.__add_chart(figure=self.figure,points_for_scatter=points_for_scatter,points_for_plot=points_for_plot,title=title,xlabel=xlabel,ylabel=ylabel,ylabel2=ylabel2,xlim=xlim,ylim=ylim,y2lim=y2lim,fontsize=fontsize,color_ticklabels=color_ticklabels, color_fig=color_fig, color_axes=color_axes)
    # def get_figure(self):
    #     return self.figure
    
    def __add_chart(self,figure=None,points_for_scatter=[],points_for_plot=[],title='',xlabel='',ylabel='',ylabel2='',xlim=np.nan,ylim=np.nan,y2lim=np.nan,fontsize='medium', color_ticklabels='', color_fig='', color_axes='',figure_size=(10,6),dpi=100):
        
        if figure == None:
            self.list_of_axes=[]
            self.figure=plt.figure(figsize=figure_size,dpi=dpi)
            _axes=self.figure.add_axes([self.left_margin, self.bottom_margin, 1-self.left_margin*2, 1-self.bottom_margin*2])
            self.list_of_axes.append(_axes)        
            self.n_of_axes=len(self.list_of_axes)
        else:
            self.n_of_axes+=1
            
        if self.n_of_axes>1:
            dH=(1-self.margin_between_axes*(self.n_of_axes-1)-self.bottom_margin*2)/(self.n_of_axes)#высота одного графика
            _axes=self.figure.add_axes([self.left_margin, self.bottom_margin, 1-self.left_margin*2, dH])
            self.list_of_axes.insert(0,_axes)
            for i,_ax in enumerate(self.list_of_axes):
                _ax.set_position([self.left_margin, self.bottom_margin+dH*i+self.margin_between_axes*i, 1-self.left_margin*2, dH])

        

        _axes.set_title(title,fontsize=fontsize)
        _axes.set_xlabel(xlabel,fontsize=fontsize)
        _axes.set_ylabel(ylabel,fontsize=fontsize)
        # _axes.set_xticklabels(fontsize=fontsize)
        _axes.tick_params(axis='both', labelsize=fontsize, colors=color_ticklabels) #размер числовых подписей у осей координат
        # _axes.tick_params(axis='y', labelsize=fontsize)
        # plt.style.context('dark_background')
        # _axes.tick_params(axis='x', colors='red')
        # _axes.xaxis.label.set_color('green')
        # _axes.set_xticklabels(self, labels, *, fontdict=None, minor=False, **kwargs)
        # _axes.set_xticklabels(color='green')
        self.figure.set_facecolor(color_fig)
        _axes.set_facecolor(color_axes)
        if not (xlim is np.nan):
            _axes.set_xlim(xlim)
        if not (ylim is np.nan):
            _axes.set_ylim(ylim)
    
        
        for _array in points_for_plot:
            _x=_array.get('x')
            _y=_array.get('y')
            _y2=_array.get('y2')
            _label=_array.get('label')
            _lw=_array.get('lw')
            _c=_array.get('c')
            _ls=_array.get('ls')
            if not _y is None:
                _axes.plot(_x,_y,label=_label,lw=_lw,color=_c,ls=_ls,zorder=1)
            elif not _y2 is None:
                _axes2 = _axes.twinx()
                _axes2.plot(_x,_y2,label=_label,lw=_lw,color=_c,ls=_ls,zorder=1)
                _axes2.set_ylabel(ylabel2)
                if not (y2lim is np.nan):
                    _axes2.set_ylim(y2lim)
                _axes2.legend()
                
        for _array in points_for_scatter:
            _x=_array.get('x')
            _y=_array.get('y')
            _y2=_array.get('y2')
            _label=_array.get('label')
            _s=_array.get('s')
            _marker=_array.get('marker')
            _c=_array.get('c')
            if not _y is None:
                _axes.scatter(_x,_y,label=_label,s=_s,marker=_marker,color=_c,zorder=2)
            elif not _y2 is None:
                _axes2=_axes.twinx()
                _axes2.scatter(_x,_y2,label=_label,s=_s,marker=_marker,color=_c,zorder=2)
                _axes2.set_ylabel(ylabel2)
                if not (y2lim is np.nan):
                    _axes2.set_ylim(y2lim)
                # _axes.twinx().legend()
                
        if len(_axes.get_legend_handles_labels()[0])!=0:
            _axes.legend()
        _axes.grid()




"""
# ДЛЯ ТЕСТОВ:
import matplotlib.pyplot as plt
# import graphics as gr
# fig= plt.figure()

# axes= fig.add_axes([0.1,0.1,0.8,0.8])
x=[1,2,3]
y=[2,4,8]
x2=[3,4,7]
y2=[1,5,9]

Fig=Chart(points_for_scatter=[{'x':x,'y':y,'label':'11111'}],points_for_plot=[{'x':x,'y':y,'label':'121212'}],title='111111',xlabel='A',ylabel='B',color_ticklabels='yellow', color_fig='black', color_axes='gray',dpi=150,figure_size=(5,5))
plt.show()

Fig.add_chart(points_for_scatter=[{'x':x,'y':y,'label':'2222'}],points_for_plot=[{'x':x,'y':y,'label':'21212121'}],title='22222',xlabel='A',ylabel='B')
# pass
Fig.add_chart(points_for_scatter=[{'x':x,'y':y,'label':'sdklfjh'},{'x':x,'y2':y,'label':'y2'}],points_for_plot=[{'x':x,'y':y,'label':'sdklfjh'}],title='333',xlabel='A',ylabel='B',figure_size=(20,6),dpi=100)
# Fig=gr.make_chart(figure=Fig,points_for_scatter=[{'x':x,'y':y,'label':'sdklfjh'}],points_for_plot=[{'x':x,'y':y,'label':'sdklfjh'}],title='quiwdyegfojasg',xlabel='A',ylabel='B',figure_size=(10,6),dpi=100)
# gr.make_chart(figure=Fig,points_for_scatter=[{'x':x,'y':y,'label':'sdklfjh'}],points_for_plot=[{'x':x,'y':y,'label':'sdklfjh'}],title='quiwdyegfojasg',xlabel='A',ylabel='B',figure_size=(10,6),dpi=100)
# Fig.subplots_adjust(left = 0.125, right = 0.9,bottom = 0.1, top = 0.9, wspace = 0.1,hspace = 0.1)

# axes.plot(x,y)
# axes2= fig.add_axes([0.1,0.1,0.8,0.8])
# axes2.plot(x,y)

# fig.show()
"""