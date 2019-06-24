import math
import matplotlib.pyplot as plt

with open('Cities.txt') as inf:
    file_data = []
    for line in inf:
        line = line.strip().split()
        file_data.append(line)

cities = [i[2].lower() for i in file_data]
coordinates = {city[2].lower():{'x':city[0], 'y':city[1]} for city in file_data}

def set_starting_city(clist, starting_choice):
    if starting_choice.lower() in clist:
        index = clist.index(starting_choice.lower())
        clist[0],clist[index] = clist[index],clist[0]
        return clist
    else:
        print('{} is not a valid location'.format(starting_choice.title()))

def create_tour(clist, index=0):
    copy = clist[:]
    if index > (len(copy)-2):
        copy.append(copy[0])
        return copy
    else:
        next_city_index = (find_index(copy[index:]) + index)
        copy[index+1], copy[next_city_index] = copy[next_city_index], copy[index+1]
        index += 1
        return create_tour(copy, index)

def find_index(clist):
    current_city = clist[0]
    shortest_city = clist[1]
    shortest_distance = distance_to(current_city, shortest_city)
    for city in clist[1:]:
        current_distance = distance_to(current_city, city)
        if current_distance < shortest_distance:
            shortest_city = city
            shortest_distance = current_distance
    return clist.index(shortest_city)

def distance_to(cstart, cend):
    start_x, start_y = int(coordinates[cstart]['x']), int(coordinates[cstart]['y'])
    end_x, end_y = int(coordinates[cend]['x']), int(coordinates[cend]['y'])
    distance_x = abs(end_x-start_x)
    distance_y = abs(end_y-start_y) 
    distance = math.sqrt((distance_x)**2 + (distance_y)**2)
    return distance

def total_distance(tour):
    total_distance = 0
    for i in range(len(tour)-1):
        total_distance += distance_to(tour[i],tour[i+1])
    return(round(total_distance))

def draw_tour(tour):
    for i in range(len(tour)-1):
        current_city, next_city = tour[i], tour[i+1]
        start_x, start_y = int(coordinates[current_city]['x']), int(coordinates[current_city]['y'])
        end_x, end_y = int(coordinates[next_city]['x']), int(coordinates[next_city]['y'])   
        # Draw dots representing cities
        plt.plot(start_x,-start_y, 'ro')
        # Add label to each dot
        if current_city == tour[0]:
            plt.text(start_x,-start_y,'{} (Start)'.format(current_city.title()),weight="bold")
        else:
            plt.text(start_x,-start_y,current_city.title())
        # Draw lines between cities    
        plt.plot([start_x,end_x],[-start_y,-end_y],'k-')

    distance = total_distance(tour)
    # Annotate distance
    plt.text(10, 0, s='Total distance: {}'.format(distance), weight="bold")
    plt.axis('equal')
    plt.show()
        
def optimal_tour(clist):
    copy = clist[:]
    shortest_tour = create_tour(copy)
    shortest_distance = total_distance(shortest_tour)
    for city in copy:
        set_starting_city(copy, city)
        new_tour = create_tour(copy)
        distance = total_distance(new_tour)
        print(new_tour[0], distance)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_tour = new_tour
    return shortest_tour

#set_starting_city(cities, 'glasgow')
#draw_tour(create_tour(set_starting_city(cities, 'glasgow')))
shortest_tour = optimal_tour(cities)
draw_tour(shortest_tour)
