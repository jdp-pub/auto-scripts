import requests
import axc




def main():
    # select topics
    catl = ["physics", "math"]

    top1 = [
        "quantum computer speed limits",
        "Characterizing post-selected quantum dynamics and its classical counterparts",
        "Spatio-temporal correlations quantum mechanics"
        ]

    top2 = [
        "percolation theory",
        "differential equation phase diagrams",
    ]

    keys = []

    
    keys = [(catl[0],i) for i in top1] + [(catl[1],i) for i in top2]


    # get topic list
    print("beggining query...")
    a = axc.query(keys)
    keys = axc.clean(keys, "_")

    # write selected topics to pdf
    print("\nexporting...")
    axc.export(keys, a)


if __name__ == '__main__':
    main()