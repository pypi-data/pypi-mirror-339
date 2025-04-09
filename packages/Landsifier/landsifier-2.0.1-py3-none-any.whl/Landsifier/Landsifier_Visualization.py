from Landsifier_DataPreparation import *
from Landsifier_ML_Training import *
from Landsifier_Prediction import *


def get_image_data(probability, path):
    
    dictionary = load_data(path)
    data=np.int32(np.asarray(probability)*100)    
    image_data=np.zeros((100,len(data)))
    
    for i in range(len(data)):
        a1,b1,c1=data[i][0],data[i][0]+data[i][1],data[i][0]+data[i][1]+data[i][2]
        image_data[0:a1,i]=0
        image_data[a1:b1,i]=1
        image_data[b1:c1,i]=2
        image_data[c1:100,i]=3
        
        
    images = {}
    for key in dictionary.keys():
        names = f'ind_{key}'
        images[names] = np.array([])
    
        
    for i in range(np.shape(image_data)[1]):
        n=np.shape(image_data)[1]
        dat=image_data[:,i]
        
        for j, keys in enumerate(images.keys()):
            images[keys] = np.argwhere(dat == j)[:,0]
        # print('shape of images ::', np.shape(images[keys]))
            

        indices = np.hstack([images[names] for names in images.keys()])
        temp_array = np.zeros_like(image_data[:,i])
        if (i>0) & (i<int(n/4)):
            temp_array[indices] = image_data[:,i][indices]
            
        elif (i>int(n/4)) & (i<int(n/2)):
            temp_array[indices] = image_data[:,i][indices]
            
        elif (i>int(n/2)) & (i<int(3*n/4)):
            temp_array[indices] = image_data[:,i][indices]
            
        elif (i>int(3*n/4)) & (i<int(n)):
            temp_array[indices] = image_data[:,i][indices]
        
    image_data[:,i] = temp_array
    image_data = np.int32(image_data)
    image = np.dstack((image_data, image_data, image_data))
            
            
    colors_rgb = {
    'red': (215, 25, 28),
    'green': (0, 255, 0),
    'blue': (44, 123, 182),
    'yellow': (255, 255, 0),
    'cyan': (171, 217, 233),
    'magenta': (255, 0, 255),
    'orange': (253, 141, 60),
    'purple': (128, 0, 128),
    'brown': (165, 42, 42),
    'pink': (255, 192, 203)
    }
    
    colour_labels = []
    
    for j, key in enumerate(images.keys()):
        available_colors = list(colors_rgb.keys())
        selected_color = random.sample(available_colors,1)[0]
        colour = colors_rgb[selected_color]
        colour = list(colour)
        colour2 = [colour[i]/255 for i in range(len(colour))]
        colour_labels.append(colour2)
        print(colour)
        
        image[image_data[:,:] == j] = colour           ### (issue)
        
    
    image=np.int32(image) 
    print(np.max(image))
    import matplotlib as mpl
    
    
    fig=plt.figure(dpi=100)
    fig.set_size_inches(18.5, 10.5)

    plt.subplot(221)
    print(colour_labels)    
    
    
    cm = mpl.colors.ListedColormap(colour_labels)
    pcm=plt.imshow(image,cmap=cm,aspect='auto',origin='lower')
    
    cb=plt.colorbar(pcm, location='top',pad=0.07)
    cb.set_ticks([])
    plt.ylabel('Class Probability',fontsize=28)
    plt.xlabel('Test  Sample Index',fontsize=28)
    plt.show()