import gpxpy.gpx
import datetime
from geopy.distance import distance


def run(activity_gpx, maximumSpeedAsPaused = 0.25): # We set the default value as 0.25

    gpx = activity_gpx
    removed = datetime.timedelta()
    last = None
    start = None
    stops = 0
    tot_dist = 0.
    ret_data = {}
    elapsedTime = datetime.timedelta()

    for track in gpx.tracks:
        for segment in track.segments:
            for i, point in enumerate(segment.points):
                time = point.time
                if i == 0:
                    start = time
                if last is not None:
                    last -= elapsedTime.total_seconds()
                    print('Check i={}: time={}, time-removed={}, last={}'.format(i, time, time - removed, last))
                time -= removed
                if last is not None:
                    last_point = segment.points[i-1]
                    d = distance((point.latitude, point.longitude), (last_point.latitude, last_point.longitude)).m
                    #if time - last > datetime.timedelta(seconds=1):
                    # if absolute distance travelled is less than 3m, then the recording could have paused.
                    # time - last must be positive, or td_to_str() will crash.
                    #if (abs(d) < 3) and ((time - last) > datetime.timedelta(seconds=0)):
                    elapsedTime = time - last
                    #print('time={}, last={}, elapsed={}'.format(time, last, elapsedTime))
                    if ((time - last) > datetime.timedelta(seconds=0)):
                        speed = abs(d) / (time - last).total_seconds()
                        # use speed instead of absolute distance travelled. if speed is <= maximumSpeedAsPaused then the recording could have paused.
                        if (speed <= maximumSpeedAsPaused):
                            print('Pause {}: {}s | {:.3f}m'.format(stops+1, time - last, d))
                            ret_data['Pause {}'.format(stops+1)] = [time - last, d]
                            removed += time - last
                            stops += 1
                        else:
                            tot_dist += d
                    else:
                        tot_dist += d
                if removed > datetime.timedelta():
                    gpx.tracks[0].segments[0].points[i].time = time - removed
                last = time

    print('Elapsed time: {}s'.format(last - start + removed))
    print('Moving time: {}s'.format(last - start))
    print('Paused time: {}s'.format(removed))
    print('Total distance: {:.3f}m'.format(tot_dist/1000.))
    ret_data['Elapsed time'] = last - start + removed
    ret_data['Moving time'] = last - start
    ret_data['Total distance'] = tot_dist/1000.
    ret_data['Paused time'] = removed
    gpx_xml = gpx.to_xml()
    return gpx_xml, ret_data


if __name__ == '__main__':
    activity_gpx = 'gpx/activity_177944060.gpx'
    gpx_file = open(activity_gpx, 'r')
    gpx = gpxpy.parse(gpx_file)
    activity_name = activity_gpx.split('.')[0] + '_clean.gpx'
    gpx_xml, data = run(gpx)
    with open(activity_name, 'w') as f:
        f.write(gpx_xml)
    print('Created {}'.format(activity_name))
