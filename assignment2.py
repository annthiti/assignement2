import os

def getMaxCoverageIfFireOne(input):
    input_list = input.split('\n')
    guard_count = int(input_list[0])
    last_guard_index = guard_count + 1
    guard_info_list = map(lambda x: x.split(' '), input_list[1:last_guard_index])

    # Create a schedule table
    guard_schedule = {}
    for guard_id, guard_info in enumerate(guard_info_list):
        [start, end] = [int(guard_info[0]), int(guard_info[1])]
        if not guard_schedule.get(start):
            guard_schedule[start] = {'start': [], 'end': []}
        if not guard_schedule.get(end):
            guard_schedule[end] = {'start': [], 'end': []}
        guard_schedule[start]['start'].append(guard_id)
        guard_schedule[end]['end'].append(guard_id)

    sorted_guard_schedule = dict(sorted(guard_schedule.items()))

    # Iterate through the schedule table to find coverage time
    guard_on_previous_duty = {}
    guard_on_duty_time = 0
    alone_time_table = {}
    for time, schedule in sorted_guard_schedule.items():
        if len(guard_on_previous_duty) >= 1:
            previous_shift_time = time - previous_time
            guard_on_duty_time += previous_shift_time
            if len(guard_on_previous_duty) == 1:
                guard_id = next(iter(guard_on_previous_duty))
                if not alone_time_table.get(guard_id):
                    alone_time_table[guard_id] = previous_shift_time
                else:
                    alone_time_table[guard_id] += previous_shift_time

        for guard_id in schedule['start']:
            guard_on_previous_duty[guard_id] = True

        for guard_id in schedule['end']:
            del guard_on_previous_duty[guard_id]

        previous_time = time

    # Get minimum alone time
    if (len(alone_time_table)) < guard_count:
        min_alone_time = 0 # When there's more than 1 guard to choose to be fired
    else:
        min_alone_time = min(alone_time_table.values())

    # Return maximum coverage time when fire 1 guard that has minimum alone time
    return guard_on_duty_time - min_alone_time


def run():
    CURR_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_DIR = os.path.join(CURR_DIR, 'Input')
    OUTPUT_DIR = os.path.join(CURR_DIR, 'Output')
    for file_name in sorted(os.listdir(INPUT_DIR)):
        data = open(os.path.join(INPUT_DIR, file_name), 'r').read()
        output = str(getMaxCoverageIfFireOne(data))
        with open(os.path.join(OUTPUT_DIR, file_name.replace('in','out')), 'w') as o:
            o.write(output)

run()
