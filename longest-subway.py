from datetime import datetime
import json
import random
import signal


def load_json_from_file(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def signal_handler(signal, frame):
    walker.print_progress()


def route_map(x):
    via = x['via']
    from_station = x['from']
    to_station = x['to']
    line = nodes['segments'][str(via)]['lines']

    from_station = nodes['stations'][str(from_station)]['name']
    to_station = nodes['stations'][str(to_station)]['name']

    if '_' in from_station:
        from_station = from_station['_']
    else:
        from_station = from_station[line[0]]

    if '_' in to_station:
        to_station = to_station['_']
    else:
        to_station = to_station[line[0]]

    result = {
        'line': line,
        'from': from_station,
        'to': to_station
    }

    return result


def get_overlap(a, b):
    overlap = ''
    for c in a:
        if c in b:
            overlap = overlap + c

    return overlap


def simplify(route):
    simplified = []
    for stop in route:
        if simplified:
            overlap = get_overlap(stop['line'], simplified[-1]['line'])
            if overlap:
                simplified[-1]['to'] = stop['to']
                simplified[-1]['line'] = overlap
                continue

        simplified.append(stop)

    return simplified


class GraphWalker:
    def __init__(self):
        self.dead_ends = 0

        self.distance = 0
        self.route = []

        self.max_distance = 0
        self.max_route = []

    def print_progress(self):
        self.print_route()
        print('')
        print('Traversed ' + str(self.dead_ends) + ' routes')
        print('Longest route so far: ' + str(self.max_distance) + ' feet')
        print('Current route length: ' + str(self.distance) + ' feet')

    def print_route(self):
        print('Current longest route:')
        mapped_steps = map(route_map, self.max_route)
        mapped_steps = simplify(mapped_steps)

        is_start = True
        last_step = None

        for step in mapped_steps:
            if is_start:
                print('[#] Start at ' + step['from'])
                is_start = False
            elif last_step and step['from'] != last_step['to']:
                print('[#] Transfer to ' + step['from'])

            print('[#] Take the ' + step['line'] + ' to ' + step['to'])
            last_step = step

    def traverse_from_start(self, start_station):
        start_station = str(start_station)
        self.sort_segments()

        first_step = self.first_step(start_station)
        self.route.append(first_step)

        station_names = nodes['stations'][start_station]['name']
        start_name = station_names.itervalues().next()
        print('Starting from ' + start_name)

        via = self.route[0]['via']
        self.distance = nodes['segments'][str(via)]['distance']
        self.walk()

    def walk(self):
        can_step = True
        while can_step is True:
            stepped_forward = self.step_forward()
            if stepped_forward is True:
                continue

            self.dead_end()
            can_step = self.step_backward()

    def step_forward(self, min_index=-1):
        last_step = self.route[-1]
        current_station = last_step['to']

        segments_used = map(lambda x: x['via'], self.route)
        all_segments = nodes['stations'][str(current_station)]['segments']
        segments_available = [x for x in all_segments
                              if x not in segments_used and
                              all_segments.index(x) > min_index]

        if segments_available:
            first_segment = segments_available[0]
            destinations = nodes['segments'][str(first_segment)]['ends']
            destinations = [x for x in destinations if x != current_station]
            destination = destinations[0]

            self.route.append({
                'from': current_station,
                'to': destination,
                'via': segments_available[0]
            })

            segment = nodes['segments'][str(segments_available[0])]
            self.distance = self.distance + segment['distance']

            return True

        return False

    def step_backward(self):
        last_element = None
        index = None

        while self.route:
            last_element = self.route.pop()

            station = nodes['stations'][str(last_element['from'])]
            segments = station['segments']
            index = segments.index(last_element['via'])

            this_segment = nodes['segments'][str(last_element['via'])]
            this_distance = this_segment['distance']
            self.distance = self.distance - this_distance

            can_step_forward = self.step_forward(index)
            if can_step_forward:
                return True

        return False

    def dead_end(self):
        self.dead_ends = self.dead_ends + 1
        if (self.distance <= self.max_distance):
            return False

        self.max_distance = self.distance
        self.max_route = self.route[:]

        print('')
        print('[' + str(datetime.now()) + ']')
        print('Found a new maximum subway route, report progress for details')
        print('distance = ' + str(self.max_distance))
        print('')

    def first_step(self, start):
        segment = nodes['stations'][str(start)]['segments'][0]
        ends = nodes['segments'][str(segment)]['ends']
        ends = [x for x in ends if str(x) != start]
        end = ends[0]

        data = {
            'from': start,
            'to': end,
            'via': segment
        }

        return data

    def sort_segments(self):
        for station_id in nodes['stations']:
            station = nodes['stations'][station_id]

            if random.random() < 0.25:
                station['segments'] = sorted(station['segments'])
            else:
                random.shuffle(station['segments'])


nodes = load_json_from_file('graph.json')
start_stations = [9, 80, 1, 29, 83, 69, 33, 41, 59, 5, 20]

# For pruned json:
#start_stations = [9, 80]

random.shuffle(start_stations)
walker = GraphWalker()

signal.signal(signal.SIGINT, signal_handler)
while True:
    start_station = start_stations.pop(0)
    start_stations.append(start_station)

    walker.traverse_from_start(start_station)
