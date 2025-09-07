import pygame
import random
from PIL import Image
import os

def translator(number, x): #number to (x, y)
    new_x = (number % x)
    new_y = (number // x)
    return(new_x, new_y)

def transformer(x, y, w): #(x, y) to number
    return(y * w + x)

def get_image_dict():
    values = dict()
    img_path = os.path.join('Green.jpg')
    img = Image.open(img_path).convert('RGB')

    w, h = img.size
    img = img.resize((w // 2, h // 2))
    w, h = img.size
    pixels = img.load()
    for i in range((w * h)):
        values[i] = pixels[translator(i, w)]
    return [values, w, h]

def main():
    loops = 18
    population = 85
    gens = 7
    values, w, h = get_image_dict()
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.set_caption('image simplifier')

    def visualizer():
        for i in range(w * h):
            x, y = translator(i, w)
            pygame.draw.rect(screen, values[i], pygame.Rect(x * 1, y * 1, 1, 5))
        pygame.display.flip()
    
    def rate(all_gens): #compares whole image to generated image
        counter = 0
        for key in all_gens:
            val = values[key]
            counter += abs(val[0] - all_gens[key][0]) + abs(val[1] - all_gens[key][1]) + abs(val[2] - all_gens[key][2])
        return counter

    def intersect(x:tuple, y:tuple) -> list:
        x1, y1 = x
        x2, y2 = y
        # Clamp to image bounds
        x1 = max(0, min(x1, w - 1))
        x2 = max(0, min(x2, w - 1))
        y1 = max(0, min(y1, h - 1))
        y2 = max(0, min(y2, h - 1))
        cords_list = [(xi, yi) for xi in range(min(x1, x2), max(x1, x2) + 1)
                            for yi in range(min(y1, y2), max(y1, y2) + 1)]
        return cords_list

    def mutate(fella:list, params:tuple, cols:tuple) -> list:
        new_r = min(255, max(0, fella[0] + random.randint(cols[0], cols[1])))
        new_g = min(255, max(0, fella[1] + random.randint(cols[0], cols[1])))
        new_b = min(255, max(0, fella[2] + random.randint(cols[0], cols[1])))
        new_x1 = min(w-1, max(0, fella[3][0] + random.randint(params[0], params[1])))
        new_y1 = min(h-1, max(0, fella[3][1] + random.randint(params[0], params[1])))
        new_x2 = min(w-1, max(0, fella[4][0] + random.randint(params[0], params[1])))
        new_y2 = min(h-1, max(0, fella[4][1] + random.randint(params[0], params[1])))
        return [new_r, new_g, new_b, (new_x1, new_y1), (new_x2, new_y2)]

    def evolve():
        best_ni = None
        best_dih = 676767676767676767676767676767
        for gen in range(gens):
            print(gen)
            if gen > 0:
                for i in range(population):
                    pop[i] = mutate(best_ni, (round(-w / gens), round(w / gens)), (-20, 20))
            for cre in pop: #cre = key of dict
                temp_ag = my_image.copy() #has list of w*h amount
                tects = intersect(pop[cre][3], pop[cre][4])
                for t in tects: #t = tuple xy
                    temp_ag[transformer(t[0], t[1], w)] = (pop[cre][0], pop[cre][1], pop[cre][2]) #overlaps current ag
                check = rate(temp_ag)
                if check < best_dih:
                    best_dih = check
                    best_ni = pop[cre]
            print(f'best_ni: {best_ni}') #best_ni is a list
        return best_ni, intersect(best_ni[3], best_ni[4]), (best_ni[0], best_ni[1], best_ni[2])
    
    #Main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        #the line
        my_image = dict()
        for i in range(w * h):
            my_image[i] = (0, 0, 0)
        for loop in range(loops):
            print(f'loop: {loop}')
            pop = dict()
            for c in range(population):
                pop[c] = [random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255), (random.randint(0, w),
                                random.randint(0, h)), (random.randint(0, w),
                                random.randint(0, h))]
            my_fella, tersects, color = evolve()
            for inter in tersects: #inter is a tuple; the cords
                my_image[transformer(inter[0], inter[1], w)] = color
            x1, y1 = my_fella[3]
            x2, y2 = my_fella[4]
            rectni = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
            pygame.draw.rect(screen, (my_fella[0], my_fella[1], my_fella[2]), rectni)
            pygame.display.flip()
        pygame.image.save(screen, 'saved_screen.png')


if __name__ == '__main__':
    main()