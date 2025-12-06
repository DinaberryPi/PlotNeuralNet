import sys
sys.path.append('../')
from pycore.tikzeng import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),
    
    # Input
    to_input('../examples/input.png', to='(-3,0,0)', width=8, height=8, name="input"),
    
    # Backbone
    to_ConvConvRelu(name='backbone', s_filer=320, n_filer=(64,128,1280), 
                     offset="(0,0,0)", to="(0,0,0)", 
                     width=(4,6,8), height=30, depth=30, 
                     caption="EfficientNet-B0"),
    to_connection("input", "backbone"),
    
    # GAP
    to_Pool(name="gap", offset="(1,0,0)", to="(backbone-east)", 
            width=1, height=25, depth=25, caption="GAP\\\\1280"),
    to_connection("backbone", "gap"),
    
    # Features 1280-dim block (central hub)
    to_Conv(name='features', s_filer=1280, n_filer=1280, 
            offset="(1.5,0,0)", to="(gap-east)", 
            width=3, height=25, depth=25, caption="Features\\\\1280-dim"),
    to_connection("gap", "features"),
    
    # Class Head: MLP + Output
    to_Conv(name='class_mlp', s_filer=1280, n_filer=512, 
            offset="(2,8,0)", to="(features-east)", 
            width=2.5, height=20, depth=20, caption="512 Class\\\\MLP"),
    to_Conv(name='class_output', s_filer=512, n_filer=3, 
            offset="(1,0,0)", to="(class_mlp-east)", 
            width=1.5, height=8, depth=8, caption="Class\\\\(3)"),
    to_connection("features", "class_mlp"),
    to_connection("class_mlp", "class_output"),
    
    # Order Head: MLP + Output
    to_Conv(name='order_mlp', s_filer=1283, n_filer=512, 
            offset="(0,-5,0)", to="(class_mlp-south)", 
            width=2.5, height=20, depth=20, caption="512 Order\\\\MLP"),
    to_Conv(name='order_output', s_filer=512, n_filer=2, 
            offset="(1,0,0)", to="(order_mlp-east)", 
            width=1.5, height=6, depth=6, caption="Order\\\\(2)"),
    to_connection("features", "order_mlp"),
    to_connection("class_output", "order_mlp"),  # Cascade from Class
    to_connection("order_mlp", "order_output"),
    
    # Family Head: MLP + Output
    to_Conv(name='family_mlp', s_filer=1285, n_filer=512, 
            offset="(0,-5,0)", to="(order_mlp-south)", 
            width=2.5, height=20, depth=20, caption="512 Family\\\\MLP"),
    to_Conv(name='family_output', s_filer=512, n_filer=3, 
            offset="(1,0,0)", to="(family_mlp-east)", 
            width=1.5, height=8, depth=8, caption="Family\\\\(3)"),
    to_connection("features", "family_mlp"),
    to_connection("order_output", "family_mlp"),  # Cascade from Order
    to_connection("family_mlp", "family_output"),
    
    # Genus Head: MLP + Output
    to_Conv(name='genus_mlp', s_filer=1288, n_filer=1024, 
            offset="(0,-5,0)", to="(family_mlp-south)", 
            width=3, height=24, depth=24, caption="1024 Genus\\\\MLP"),
    to_Conv(name='genus_output', s_filer=1024, n_filer=24, 
            offset="(1,0,0)", to="(genus_mlp-east)", 
            width=2, height=12, depth=12, caption="Genus\\\\(24)"),
    to_connection("features", "genus_mlp"),
    to_connection("family_output", "genus_mlp"),  # Cascade from Family
    to_connection("genus_mlp", "genus_output"),
    
    # Species Head: MLP + Output
    to_Conv(name='species_mlp', s_filer=1312, n_filer=1024, 
            offset="(0,-5,0)", to="(genus_mlp-south)", 
            width=3, height=24, depth=24, caption="1024 Species\\\\MLP"),
    to_Conv(name='species_output', s_filer=1024, n_filer=82, 
            offset="(1,0,0)", to="(species_mlp-east)", 
            width=2.5, height=18, depth=18, caption="Species\\\\(82)"),
    to_connection("features", "species_mlp"),
    to_connection("genus_output", "species_mlp"),  # Cascade from Genus
    to_connection("species_mlp", "species_output"),
    
    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()
