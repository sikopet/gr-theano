#!/usr/bin/env python
import numpy
import theano
import theano.tensor as T
import time
#rng = numpy.random






# GNU Radio block
import numpy
from gnuradio import gr, blocks, audio
class siggen(gr.sync_block):

    # some consts
    N = 4096
#    fs = 44100.0;
#    tone = 400.0;

    # theano vars
    step = T.vector("step", dtype="complex64")
    l = T.iscalar("l")
    stepd = theano.shared(numpy.zeros(N, dtype=numpy.complex64), name="stepd")
    phase = theano.shared(numpy.asarray(1+0j, dtype=numpy.complex64), name="phase")

    # theano mappings
    oo = phase * stepd;
    oos = oo[0:l]

    # theano functions
    set_step = theano.function(
            inputs=[step],
            outputs=[],
            updates={stepd:step},
            name="set_step")
    rval = theano.function(
            inputs=[l],
            outputs=[oos],
            updates={phase:oo[l-1]*stepd[1]},
            name="rval")

    def set_f(self, f):
        print "set_f %f"%(f)
        self.f = f;
        
        # set up step table
        stepval = numpy.pi*2*self.f/self.fs;
        iv = numpy.exp(1j*numpy.arange(0,self.N,stepval, dtype=numpy.float32) , dtype=numpy.complex64);
        self.set_step( iv );

    def __init__(self, fs, f):
        gr.sync_block.__init__(self,
            name="theano_siggen",
            in_sig=[],
            out_sig=[numpy.complex64])
        self.fs = fs
        self.set_f(f);


    def work(self, input_items, output_items):
        out = output_items[0]
        out[:] = self.rval(len(output_items[0]))[0];
        return len(output_items[0])



