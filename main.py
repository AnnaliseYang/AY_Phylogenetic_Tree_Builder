from display_window import PhylogeneticWindow as PW

which_window = 1    # 1, 2

match which_window:
    case 1:
        PW().run()
    case 2:
        PW(1).run()
    case _:
        PW().run()
