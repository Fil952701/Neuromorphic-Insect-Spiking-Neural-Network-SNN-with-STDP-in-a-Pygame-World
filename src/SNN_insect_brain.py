import numpy as np
import brian2 as b
import matplotlib.pyplot as plt

# ——— 1) Scope e clock ———
b.start_scope()
b.defaultclock.dt = 0.1 * b.ms

'''print("Test Poisson Group:")
PG = b.PoissonGroup(1, rates=500*b.Hz)
M  = b.SpikeMonitor(PG)
net = b.Network(PG, M)
print("prima run:", float(b.defaultclock.t/b.ms), "ms")
net.run(200*b.ms)
print("dopo run:",  float(b.defaultclock.t/b.ms), "ms")
print("Spike count:", M.count[:])
print("Fine test.")'''

# ——— 2) Parametri generali ———
n_inputs, n_outputs = 8, 8

# ——— 3) PoissonGroup come sensori d’odore ———
# rates verranno aggiornati in step_snn()
poisson_group = b.PoissonGroup(n_inputs, rates=0 * b.Hz)

# ——— 4) Neuroni di output ———
output_group = b.NeuronGroup(
    n_outputs,
    model='dv/dt = -v/(10*ms) : 1',
    threshold='v > 0.05',
    reset='v = 0',
    method='exact'
)

# ——— 5) STDP one-to-one ———
synapses = []
syn = b.Synapses(
    poisson_group, output_group,
    model='''
        w : 1
        dapre/dt  = -apre/(20*ms)  : 1 (event-driven)
        dapost/dt = -apost/(20*ms) : 1 (event-driven)
    ''',
    on_pre='''
        v_post += w
        apre    += 0.01
        w       = clip(w + apost, 0, 1)
    ''',
    on_post='''
        apost   += -0.0105
        w        = clip(w + apre, 0, 1)
    '''
)
syn.connect(j='i')
#syn.w = '0.5 + 0.5*rand()'    # o inizializza a 1.0 per test rapido

syn.w = 2.0
synapses.append(syn)
output_group.v = 0.0

# ——— 6) Monitors ———
spike_mon_in  = b.SpikeMonitor(poisson_group)
spike_mon_out = b.SpikeMonitor(output_group)
state_mon     = b.StateMonitor(syn, 'w', record=True)

# ——— 7) Network esplicito ———
net = b.Network(
    poisson_group,
    output_group,
    synapses,
    spike_mon_in,
    spike_mon_out,
    state_mon
)

def step_snn(sensor_inputs, duration=200*b.ms):
    # 1) aggiorna i tassi Poisson
    rate_q = np.array(sensor_inputs) * 1000.0 * b.Hz
    poisson_group.rates = rate_q
    print(f"  [DEBUG] rates impostate = {rate_q}")

    # 2) segna t0 e simula CON IL TUO network esplicito
    t0 = b.defaultclock.t
    net.run(duration)
    t1 = b.defaultclock.t
    print(f"  [DEBUG] simulato da {float(t0/b.ms):.1f} ms a {float(t1/b.ms):.1f} ms")

    # 3) conta gli spike in ingresso in [t0,t1]
    n_in = int(((spike_mon_in.t > t0) & (spike_mon_in.t <= t1)).sum())
    print(f"  [DEBUG] input spikes in questo step = {n_in}")

    # 4) raccogli gli spike di output in [t0,t1]
    fired = list(spike_mon_out.i[(spike_mon_out.t > t0) & (spike_mon_out.t <= t1)])
    print(f"  [DEBUG] output spikes = {fired}")

    return fired



# ——— 9) Plot utilities ———
def plot_spikes():
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.title("Input spikes")
    plt.plot(spike_mon_in.t/b.ms, spike_mon_in.i, '.k')
    plt.xlabel("Time (ms)"); plt.ylabel("Neuron index"); plt.grid(True)
    plt.subplot(1,2,2)
    plt.title("Output spikes")
    plt.plot(spike_mon_out.t/b.ms, spike_mon_out.i, '.r')
    plt.xlabel("Time (ms)"); plt.ylabel("Neuron index"); plt.grid(True)
    plt.tight_layout(); plt.show()

def plot_weights():
    plt.figure(figsize=(8,4))
    for idx in state_mon.record:
        plt.plot(state_mon.t/b.ms, state_mon.w[idx], label=f"syn{idx}")
    plt.legend(); plt.xlabel("Time (ms)"); plt.ylabel("w"); plt.title("Weights"); plt.grid(True)
    plt.tight_layout(); plt.show()
