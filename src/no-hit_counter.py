import json
from datetime import datetime
from typing import List
from dataclasses import dataclass, asdict

def load_file(path):
    with open(path, 'r') as f:
        data = json.loads(f.read())
    return data

def load_run(path='src/data/run.json'):
   return load_file(path)

def load_run_config(path='src/data/run_config.json'):
   return load_file(path)
    
def load_pb(path='src/data/pb.json'):
    try:
        return load_file(path)
    except:
        return {}

@dataclass
class Slice:
    name: str
    hits: int
    time: int

    def __init__(self, name, hits, time):
        self.name = name
        self.hits = hits
        self.time = time

@dataclass
class NoHitRun:
    run: int
    slices: List[Slice]
    pb_slices: List[Slice]
    current_slice: int
    init_time: float

    def __init__(self, run, slices, pb_slices, current_slice = 0):
        self.run = run
        self.slices = slices
        self.pb_slices = pb_slices
        self.current_slice = current_slice
        self.init_time = datetime.now().timestamp()

    def hit(self):
        self.slices[self.current_slice].hits +=1

    def next_phase(self):
        self.slices[self.current_slice].time = int(datetime.now().timestamp() - self.init_time)
        self.current_slice += 1

    def end(self):
        return len(self.slices) == self.current_slice

    def print_status(self):
        return json.dumps(asdict(self), indent=2)

def create_slices(config, sl):
    slices = sl if len(sl) != 0 else config["splits"]

    return [
        Slice(
            slice["name"], 
            0 if len(sl) == 0 else slice["hits"], 
            0 if len(sl) == 0 else slice["time"]
            ) 
        for slice in slices
    ]

def create_no_hit(run_config, pb, run):
    slices = create_slices(run_config, run)
    pb = create_slices(run_config, run_config["splits"])

    return NoHitRun(run_config["run"], slices, pb, run_config["current_slice"])

def save_state(state, path='src/data/state.json'):
    f = open(path, "w")
    f.write(state)
    f.close()

def save_pb_run(no_hit):
    run_config = {
        "run": no_hit.run,
        "current_slice": 0 if no_hit.end() else no_hit.current_slice,
        "splits": []
    }
    for i, slice in enumerate(no_hit.slices):
        pb = no_hit.pb_slices[i]
        s = no_hit.slices[i]

        if i <= no_hit.current_slice:
            run_config["splits"].append(
                asdict(
                    Slice(
                        s.name,
                        s.hits if s.hits < pb.hits else pb.hits,
                        s.time if s.time < pb.time else pb.time,
                    )
                )
            )
        else:
            run_config["splits"].append(
                asdict(
                    Slice(
                        s.name,
                        pb.hits,
                        pb.time,
                    )
                )
            )
    save_state(json.dumps(run_config,  indent=2), 'src/data/run_config.json')
    save_state(json.dumps([] if no_hit.end() else [asdict(sl) for sl in no_hit.slices],  indent=2), 'src/data/run.json')


if __name__ == '__main__':
    run_config = load_run_config()
    pb = load_pb()
    run = load_run()

    no_hit = create_no_hit(run_config, pb, run)

    save_state(no_hit.print_status())

    running = True
    while(running):
        state = input("Enter next state: ")
        # The run is over
        if state == "e":
            running = False
        # There is hit in the current state
        elif state == "h":
            no_hit.hit()
        # Goes next step
        elif state == "n":
            no_hit.next_phase()
            if no_hit.end():
                running = False

        print(no_hit.print_status())
        save_state(no_hit.print_status())
    
    no_hit.run += 1
    save_pb_run(no_hit)