from PIL import Image

input_file = r'D:\Design\animations\1\5317302.eps'
output_file = r'D:\Design\animations\1\output-%03d.png'

im = Image.open(input_file)
for i in range(im.n_frames):
    im.seek(i)
    im.save(output_file % i)
