import gpxpy.gpx
import datetime
from geopy.distance import distance

def run(activity_gpx, maximumSpeedAsPaused = 1.0): # We set the default value as 1.0

    gpx = activity_gpx
    startPointTime = None
    totalPausedTime = datetime.timedelta()
    elapsedTime = datetime.timedelta()
    lastPointTime = None
    numberOfPauses = 0
    totalDistance = 0.
    ret_data = {}

    for track in gpx.tracks:
        for segment in track.segments:
            for i, currentPoint in enumerate(segment.points):
                # Set a currentPoint's time as currentPointTime
                currentPointTime = currentPoint.time

                # If this is the first recorded point, then set startPointTime as the time for this recorded point
                if i == 0:
                    startPointTime = currentPointTime

                # Offset the currentPointTime backwards by the totalPausedTime
                currentPointTime -= totalPausedTime

                # If we are not processing the first currentPoint, then we do this.
                if lastPointTime is not None:
                    # Offset the currentPointTime backwards by the elapsedTime
                    lastPointTime = lastPointTime - datetime.timedelta(seconds=elapsedTime.total_seconds())
                    # Get the lastPoint
                    lastPoint = segment.points[i-1]
                    # Calculate the distance between the last point and the currentPointTime
                    d = distance((currentPoint.latitude, currentPoint.longitude), (lastPoint.latitude, lastPoint.longitude)).m

                    # Reset elapsedTime to nil
                    elapsedTime = datetime.timedelta()

                    # We check that currentPointTime - lastPointTime is positive, or the program will crash.
                    if ((currentPointTime - lastPointTime) > datetime.timedelta(seconds=0)):
                        # Calculate the speed to travel from the lastPointTime point to the current point
                        speed = abs(d) / (currentPointTime - lastPointTime).total_seconds()
                        # use speed instead of absolute distance travelled. if speed is <= maximumSpeedAsPaused then the recording could have paused.
                        if (speed <= maximumSpeedAsPaused):
                            #print('Pause {}: {}s | {:.3f}m'.format(numberOfPauses+1, currentPointTime - lastPointTime, d))
                            ret_data['Pause {}'.format(numberOfPauses+1)] = [currentPointTime - lastPointTime, d]
                            # Update the total totalPausedTime time
                            totalPausedTime += currentPointTime - lastPointTime
                            # Update the elapsed time between the lastPointTime point and the current point
                            elapsedTime = currentPointTime - lastPointTime
                            # Update the number of paused points
                            numberOfPauses += 1
                        else:
                            totalDistance += d
                    else:
                        totalDistance += d
                # if there was paused points in this file, then offset all points backwards by the total totalPausedTime time
                if totalPausedTime > datetime.timedelta():
                    gpx.tracks[0].segments[0].points[i].time = currentPointTime - totalPausedTime
                # Set the lastPointTime with the currentPointTime
                lastPointTime = currentPointTime

    print('Elapsed time: {}s'.format(lastPointTime - startPointTime + totalPausedTime))
    print('Moving time: {}s'.format(lastPointTime - startPointTime))
    print('Paused time: {}s'.format(totalPausedTime))
    print('Total distance: {:.3f}m'.format(totalDistance/1000.))
    ret_data['Elapsed time'] = lastPointTime - startPointTime + totalPausedTime
    ret_data['Moving time'] = lastPointTime - startPointTime
    ret_data['Total distance'] = totalDistance/1000.
    ret_data['Paused time'] = totalPausedTime
    gpx_xml = gpx.to_xml()
    return gpx_xml, ret_data

def run_v2(activity_gpx, maximumSpeedAsPaused = 1.0): # We set the default value as 1.0

    gpx = activity_gpx
    startPointTime = None
    totalPausedTime = datetime.timedelta()
    elapsedTime = datetime.timedelta()
    lastPointTime = None
    numberOfPauses = 0
    totalDistance = 0.
    ret_data = {}

    for track in gpx.tracks:
        for segment in track.segments:
            for i, currentPoint in enumerate(segment.points):
                # Set a currentPoint's time as currentPointTime
                currentPointTime = currentPoint.time

                # If this is the first recorded point, then set startPointTime as the time for this recorded point
                if i == 0:
                    startPointTime = currentPointTime

                # Offset the currentPointTime backwards by the totalPausedTime
                currentPointTime -= totalPausedTime

                # If we are not processing the first currentPoint, then we do this.
                if lastPointTime is not None:
                    # Offset the currentPointTime backwards by the elapsedTime
                    lastPointTime = lastPointTime - datetime.timedelta(seconds=elapsedTime.total_seconds())
                    # Get the lastPoint
                    lastPoint = segment.points[i-1]

                    # Calculate the distance between the last point and the currentPointTime
                    d = distance((currentPoint.latitude, currentPoint.longitude), (lastPoint.latitude, lastPoint.longitude)).m
                    
                    # Reset elapsedTime to nil
                    elapsedTime = datetime.timedelta()

                    # We check that currentPointTime - lastPointTime is positive, or the program will crash.
                    if ((currentPointTime - lastPointTime) > datetime.timedelta(seconds=0)):
                        # Calculate the speed to travel from the lastPointTime point to the current point
                        speed = abs(d) / (currentPointTime - lastPointTime).total_seconds()
                        dt = (currentPointTime - lastPointTime).total_seconds()
                        print(f'Point at ({currentPoint.latitude},{currentPoint.longitude}) -> s={speed} -> d={d} -> t={dt}')
                        # use speed instead of absolute distance travelled. if speed is <= maximumSpeedAsPaused then the recording could have paused.
                        if (speed <= maximumSpeedAsPaused):
                            print('Skipping this point')
                            #print('Pause {}: {}s | {:.3f}m'.format(numberOfPauses+1, currentPointTime - lastPointTime, d))
                            ret_data['Pause {}'.format(numberOfPauses+1)] = [currentPointTime - lastPointTime, d]
                            # Update the total totalPausedTime time
                            totalPausedTime += currentPointTime - lastPointTime
                            # Update the elapsed time between the lastPointTime point and the current point
                            elapsedTime = currentPointTime - lastPointTime
                            # Update the number of paused points
                            numberOfPauses += 1
                        else:
                            totalDistance += d
                    else:
                        totalDistance += d
                # if there was paused points in this file, then offset all points backwards by the total totalPausedTime time
                if totalPausedTime > datetime.timedelta():
                    gpx.tracks[0].segments[0].points[i].time = currentPointTime - totalPausedTime
                # Set the lastPointTime with the currentPointTime
                lastPointTime = currentPointTime

    print('Start time: {}s'.format(startPointTime))
    print('End time: {}s'.format(lastPointTime))
    print('Elapsed time: {}s'.format(lastPointTime - startPointTime + totalPausedTime))
    print('Moving time: {}s'.format(lastPointTime - startPointTime))
    print('Paused time: {}s'.format(totalPausedTime))
    print('Number of Pauses: {}'.format(numberOfPauses))
    print('Total distance: {:.3f}m'.format(totalDistance/1000.))
    ret_data['Elapsed time'] = lastPointTime - startPointTime + totalPausedTime
    ret_data['Moving time'] = lastPointTime - startPointTime
    ret_data['Total distance'] = totalDistance/1000.
    ret_data['Paused time'] = totalPausedTime
    gpx_xml = gpx.to_xml()

    return gpx_xml, ret_data

if __name__ == '__main__':
    activity_gpx = 'gpx/activity_177944060.gpx'
    gpx_file = open(activity_gpx, 'r')
    gpx = gpxpy.parse(gpx_file)
    # Process the GPX file version 1
    #activity_name = activity_gpx.split('.')[0] + '_clean.gpx'
    #gpx_xml, data = run(gpx)
    #with open(activity_name, 'w') as f:
    #    f.write(gpx_xml)
    #print('Created {}'.format(activity_name))
    # Process the GPX file version 2
    activity_name = activity_gpx.split('.')[0] + '_v2_clean.gpx'
    gpx_xml, data = run_v2(gpx)
    with open(activity_name, 'w') as f:
        f.write(gpx_xml)
    print('Created {}'.format(activity_name))
