#!usr/bin/python
from Seismogram import Seismogram
from scipy.signal import hilbert, chirp
import matplotlib.pyplot as plt
import numpy as np
import peakutils as pkt

def main():
	z = complex(3.0, 4.0)
	print z
	mod_z = np.abs(z)
	print mod_z
	comp_z = complex(z)
	print comp_z

	duration = 1.0
	fs = 400.0
	samples = int(fs*duration)
	t = np.arange(samples) / fs

	smg = Seismogram("/home/vedang/Desktop/PS/Datasets/Kachchh", "pitsa001.003", "r")
	y = smg.get_amplitudes()
	for a in y:
		a += 10000000
	bsl = pkt.baseline(y)
	y = y - bsl
	ana = hilbert(y).imag
	amp_env = (ana ** 2 + y ** 2) ** 0.5
	x = np.arange(0., smg.get_ndat() * 0.02, 0.02)

	sig = chirp(t, 20.0, t[-1], 100.0)
	sig = sig *(1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t))
	baseline_1 = pkt.baseline(sig)
	anal = hilbert(sig).imag
	amplitudes = (anal ** 2 + sig ** 2) ** 0.5

	signal = chirp(t + np.sin(2.0*np.pi*t) + t ** 2, 20.0, t[-1], 100.0)
	signal = signal *(1.0 + 0.5 * np.sin(2.0*np.pi*3.0*t)) + 5700
	baseline = pkt.baseline(signal)
	signal = signal - baseline
	analytic_function = hilbert(signal).imag
	amplitude_envelope = (analytic_function ** 2 + signal ** 2) ** 0.5

	fig = plt.figure()
	ax0 = fig.add_subplot(311)
	ax0.plot(t, sig, label='signal')
	ax0.plot(t, amplitudes, label='envelope')
#	ax0.plot(t, anal, label='hilbert')
	ax0.set_ylabel("S(t)")
	ax0.set_xlabel("t")
	ax0.legend()

	ax1 = fig.add_subplot(312)
	ax1.plot(t, signal, label='signal')	
	ax1.plot(t, amplitude_envelope, label='envelope')
#	ax1.plot(t, analytic_function, label='hilbert')
	ax1.set_ylabel("S(t)")
	ax1.set_xlabel("t")
	ax1.legend()
	
	ax2 = fig.add_subplot(313)
	ax2.plot(x, y, label='signal')
	ax2.plot(x, amp_env, label='envelope')
#	ax2.plot(x, ana, label='hilbert')
	ax2.set_xlabel("t")
	ax2.set_ylabel("S(t)")
	ax2.legend()

	plt.show()
	
if __name__ == "__main__":
	main()