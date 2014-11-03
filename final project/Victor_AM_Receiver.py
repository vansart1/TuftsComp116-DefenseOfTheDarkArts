#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Victor's AM Receiver
# Author: Victor Ansart
# Description: AM receiver from 22Mhz to 1.1 Ghz
# Generated: Tue Dec 17 19:51:38 2013
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class Victor_AM_Receiver(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Victor's AM Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.freq_fine = freq_fine = 0
		self.volume = volume = 1
		self.transition = transition = 1000000
		self.samp_rate = samp_rate = 2000000
		self.freq = freq = 24500000+freq_fine
		self.cutoff = cutoff = 100000

		##################################################
		# Blocks
		##################################################
		_volume_sizer = wx.BoxSizer(wx.VERTICAL)
		self._volume_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_volume_sizer,
			value=self.volume,
			callback=self.set_volume,
			label="Volume",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._volume_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_volume_sizer,
			value=self.volume,
			callback=self.set_volume,
			minimum=0,
			maximum=10,
			num_steps=10,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_volume_sizer, 1, 0, 1, 10)
		_transition_sizer = wx.BoxSizer(wx.VERTICAL)
		self._transition_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_transition_sizer,
			value=self.transition,
			callback=self.set_transition,
			label="Filter Transition Band",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._transition_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_transition_sizer,
			value=self.transition,
			callback=self.set_transition,
			minimum=100000,
			maximum=3000000,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_transition_sizer, 1, 26, 1, 13)
		self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Source FFT")
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Source Waterfall")
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Post-Demod FFT")
		self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "Post-Demod Waterfall")
		self.Add(self.notebook_0)
		self._freq_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.freq,
			callback=self.set_freq,
			label="Exact Frequency",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._freq_text_box, 0, 0, 1, 10)
		_cutoff_sizer = wx.BoxSizer(wx.VERTICAL)
		self._cutoff_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_cutoff_sizer,
			value=self.cutoff,
			callback=self.set_cutoff,
			label="Filter Cutoff",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._cutoff_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_cutoff_sizer,
			value=self.cutoff,
			callback=self.set_cutoff,
			minimum=1000,
			maximum=1000000,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_cutoff_sizer, 1, 11, 1, 13)
		self.wxgui_waterfallsink2_1 = waterfallsink2.waterfall_sink_c(
			self.notebook_0.GetPage(1).GetWin(),
			baseband_freq=0,
			dynamic_range=100,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
		)
		self.notebook_0.GetPage(1).Add(self.wxgui_waterfallsink2_1.win)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.notebook_0.GetPage(3).GetWin(),
			baseband_freq=0,
			dynamic_range=100,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
		)
		self.notebook_0.GetPage(3).Add(self.wxgui_waterfallsink2_0.win)
		self.wxgui_fftsink2_1 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(0).GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
		)
		self.notebook_0.GetPage(0).Add(self.wxgui_fftsink2_1.win)
		self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
			self.notebook_0.GetPage(2).GetWin(),
			baseband_freq=0,
			y_per_div=10,
			y_divs=10,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=1024,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="FFT Plot",
			peak_hold=False,
			win=window.flattop,
		)
		self.notebook_0.GetPage(2).Add(self.wxgui_fftsink2_0.win)
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + "" )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate)
		self.osmosdr_source_c_0.set_center_freq(freq, 0)
		self.osmosdr_source_c_0.set_freq_corr(0, 0)
		self.osmosdr_source_c_0.set_dc_offset_mode(0, 0)
		self.osmosdr_source_c_0.set_iq_balance_mode(0, 0)
		self.osmosdr_source_c_0.set_gain_mode(0, 0)
		self.osmosdr_source_c_0.set_gain(10, 0)
		self.osmosdr_source_c_0.set_if_gain(20, 0)
		self.osmosdr_source_c_0.set_bb_gain(20, 0)
		self.osmosdr_source_c_0.set_antenna("", 0)
		self.osmosdr_source_c_0.set_bandwidth(0, 0)
		  
		self.low_pass_filter_0 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, samp_rate, cutoff, transition, firdes.WIN_HAMMING, 6.76))
		_freq_fine_sizer = wx.BoxSizer(wx.VERTICAL)
		self._freq_fine_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_freq_fine_sizer,
			value=self.freq_fine,
			callback=self.set_freq_fine,
			label="Fine Frequency Adjust",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._freq_fine_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_freq_fine_sizer,
			value=self.freq_fine,
			callback=self.set_freq_fine,
			minimum=-2000000,
			maximum=2000000,
			num_steps=1000,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_freq_fine_sizer, 0, 11, 1, 30)
		self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
		self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((volume, ))
		self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
		self.audio_sink_0 = audio.sink(samp_rate, "", True)
		self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.wxgui_fftsink2_1, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.wxgui_waterfallsink2_1, 0))
		self.connect((self.low_pass_filter_0, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_float_0, 0))
		self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
		self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.wxgui_fftsink2_0, 0))
		self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.blocks_multiply_xx_0, 1))


	def get_freq_fine(self):
		return self.freq_fine

	def set_freq_fine(self, freq_fine):
		self.freq_fine = freq_fine
		self._freq_fine_slider.set_value(self.freq_fine)
		self._freq_fine_text_box.set_value(self.freq_fine)
		self.set_freq(24500000+self.freq_fine)

	def get_volume(self):
		return self.volume

	def set_volume(self, volume):
		self.volume = volume
		self._volume_slider.set_value(self.volume)
		self._volume_text_box.set_value(self.volume)
		self.blocks_multiply_const_vxx_0.set_k((self.volume, ))

	def get_transition(self):
		return self.transition

	def set_transition(self, transition):
		self.transition = transition
		self._transition_slider.set_value(self.transition)
		self._transition_text_box.set_value(self.transition)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))
		self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
		self.wxgui_fftsink2_1.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_1.set_sample_rate(self.samp_rate)
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.osmosdr_source_c_0.set_center_freq(self.freq, 0)
		self.analog_sig_source_x_0.set_frequency(self.freq)
		self._freq_text_box.set_value(self.freq)

	def get_cutoff(self):
		return self.cutoff

	def set_cutoff(self, cutoff):
		self.cutoff = cutoff
		self._cutoff_slider.set_value(self.cutoff)
		self._cutoff_text_box.set_value(self.cutoff)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.cutoff, self.transition, firdes.WIN_HAMMING, 6.76))

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = Victor_AM_Receiver()
	tb.Run(True)

