import matplotlib.pyplot as plt

star1 = [14, 30]
star2 = [15, 80]
star3 = [30, 20]
star4 = [75, 90]
star5 = [10, 40]


markernonactive = 'bo'
markeractive = 'rx'
# coloractive = 'r'
linecolor = 'k'

fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(9,2))
ax = [ax1, ax2, ax3, ax4]

for i in range(4):
    ax[i].axis('off')
    ax[i].plot(star1[0], star1[1], markeractive)
    ax[i].plot(star2[0], star2[1], markeractive)
    ax[i].plot([0, 100], [50, 50], linecolor)
    ax[i].plot([50, 50], [0, 100], linecolor)

    if i > 0:
        ax[i].plot(star3[0], star3[1], markeractive)
        ax[i].plot([0,  50], [25, 25], linecolor)
        ax[i].plot([25, 25], [0,  50], linecolor)
    else:
        ax[i].plot(star3[0], star3[1], markernonactive)

    if i > 1:
        ax[i].plot(star4[0], star4[1], markeractive)
    else:
        ax[i].plot(star4[0], star4[1], markernonactive)
    
    if i > 2:
        ax[i].plot(star5[0], star5[1], markeractive)
        ax[i].plot([0,  25], [37.5, 37.5], linecolor)
        ax[i].plot([12.5, 12.5], [25,  50], linecolor)    
    else:
        ax[i].plot(star5[0], star5[1], markernonactive)



fig.savefig('test.png')
# Save image




# Save image 


# Save image



# Save image