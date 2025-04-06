def main():
    import sys
    from ._viewer import Viewer
    from qtpy.QtCore import QTimer

    viewer = Viewer()

    if len(sys.argv) > 1:
        def later():
            for pos, arg in enumerate(sys.argv):
                print('Argument %d: %s' % (pos, arg))
                if pos > 0:
                    viewer.open(arg)

        QTimer.singleShot(600, later)

    import napari
    napari.run()


if __name__ == '__main__':
    main()