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

                # If this is the first recorded point, then set start as the time for this recorded point
                if i == 0:
                    start = time

                # Offset the recorded time backwards by the removed paused time
                time -= removed
                if last is not None:
                    last = last - datetime.timedelta(seconds=elapsedTime.total_seconds())
                    last_point = segment.points[i-1]
                    d = distance((point.latitude, point.longitude), (last_point.latitude, last_point.longitude)).m

                    # Reset elapsedTime to nil
                    elapsedTime = datetime.timedelta()

                    #if time - last > datetime.timedelta(seconds=1):
                    # if absolute distance travelled is less than 3m, then the recording could have paused.
                    # time - last must be positive, or td_to_str() will crash.
                    #if (abs(d) < 3) and ((time - last) > datetime.timedelta(seconds=0)):
                    #print('time={}, last={}, elapsed={}'.format(time, last, elapsedTime))
                    if ((time - last) > datetime.timedelta(seconds=0)):
                        # Calculate the speed to travel from the last point to the current point
                        speed = abs(d) / (time - last).total_seconds()
                        # use speed instead of absolute distance travelled. if speed is <= maximumSpeedAsPaused then the recording could have paused.
                        if (speed <= maximumSpeedAsPaused):
                            print('Pause {}: {}s | {:.3f}m'.format(stops+1, time - last, d))
                            ret_data['Pause {}'.format(stops+1)] = [time - last, d]
                            # Update the total removed time
                            removed += time - last
                            # Update the elapsed time between the last point and the current point
                            elapsedTime = time - last
                            # Update the number of paused points
                            stops += 1
                        else:
                            tot_dist += d
                    else:
                        tot_dist += d
                # if there was paused points in this file, then offset all points backwards by the total removed time
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
