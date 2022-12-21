from PIL import Image

x=Image.open('assets/blank.png')
x=x.resize((30,30))#sizer..
x.save('assets_solver/blank.png')
for i in range(9):
    x=Image.open('assets/n'+str(i)+'.png')
    x=x.resize((30,30))#sizer..
    x.save('assets_solver/n'+str(i)+'.png')
print('DONE')
