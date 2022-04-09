#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/ubuntu/Smart_car/src/ros_arduino_bridge-indigo-devel/ros_arduino_python"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/ubuntu/Smart_car/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/ubuntu/Smart_car/install/lib/python2.7/dist-packages:/home/ubuntu/Smart_car/build/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/ubuntu/Smart_car/build" \
    "/usr/bin/python2" \
    "/home/ubuntu/Smart_car/src/ros_arduino_bridge-indigo-devel/ros_arduino_python/setup.py" \
     \
    build --build-base "/home/ubuntu/Smart_car/build/ros_arduino_bridge-indigo-devel/ros_arduino_python" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/ubuntu/Smart_car/install" --install-scripts="/home/ubuntu/Smart_car/install/bin"
