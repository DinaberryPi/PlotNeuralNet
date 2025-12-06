import sys
sys.path.append('../')
from pycore.tikzeng import *

arch = [
    to_head('..'),
    to_cor(),
    to_begin(),
    
    # Input Image
    to_input('diatom.png', to='(-6,0,0)', width=5, height=5, name="input"),
    
    # Backbone
    to_ConvConvRelu(name='backbone', s_filer=320, n_filer=(64,128,1280), 
                     offset="(0,0,0)", to="(-4,0,0)", 
                     width=(2,3), height=40, depth=40, 
                     caption="EfficientNet-B0\\\\Backbone"),
    to_connection_with_arrow("input", "backbone"),
    
    # GAP
    to_Pool(name="gap", offset="(1.5,0,0)", to="(backbone-east)", 
            width=1, height=35, depth=35, caption="GAP"),
    to_connection_with_arrow("backbone", "gap"),
    
    # Features 1280-dim block (central hub)
    to_Conv(name='features', s_filer=1280, n_filer=1280, 
            offset="(1,0,0)", to="(gap-east)", 
            width=2, height=32, depth=32, caption="Features\\\\1280-dim"),
    to_connection_with_arrow("gap", "features"),
    
    # Class Head: MLP + Output
    to_ConvRelu(name='class_mlp', s_filer=1280, n_filer=512, 
            offset="(6,8,0)", to="(features-east)", 
            width=2.5, height=20, depth=20, caption="512\\\\Class\\\\MLP"),
    to_Conv(name='class_out', s_filer=512, n_filer=3, 
            offset="(6,0,0)", to="(class_mlp-east)", 
            width=2, height=10, depth=10, caption="Class\\\\(3)"),
    to_connection("features", "class_mlp"),
    to_connection("class_mlp", "class_out"),
    
    # Order Head: MLP + Output
    to_ConvRelu(name='order_mlp', s_filer=1283, n_filer=512, 
            offset="(0,-6,0)", to="(class_mlp-south)", 
            width=2.5, height=20, depth=20, caption="512\\\\Order\\\\MLP"),
    to_Conv(name='order_out', s_filer=512, n_filer=2, 
            offset="(6,0,0)", to="(order_mlp-east)", 
            width=2, height=8, depth=8, caption="Order\\\\(2)"),
    to_connection("features", "order_mlp"),
    to_connection("class_out", "order_mlp"),  # Cascade from Class
    to_connection("order_mlp", "order_out"),
    
    # Family Head: MLP + Output
    to_ConvRelu(name='family_mlp', s_filer=1285, n_filer=512, 
            offset="(0,-6,0)", to="(order_mlp-south)", 
            width=2.5, height=20, depth=20, caption="512\\\\Family\\\\MLP"),
    to_Conv(name='family_out', s_filer=512, n_filer=3, 
            offset="(6,0,0)", to="(family_mlp-east)", 
            width=2, height=10, depth=10, caption="Family\\\\(3)"),
    to_connection("features", "family_mlp"),
    to_connection("order_out", "family_mlp"),  # Cascade from Order
    to_connection("family_mlp", "family_out"),
    
    # Genus Head: MLP + Output
    to_ConvRelu(name='genus_mlp', s_filer=1288, n_filer=512, 
            offset="(0,-6,0)", to="(family_mlp-south)", 
            width=2.5, height=20, depth=20, caption="512\\\\Genus\\\\MLP"),
    to_Conv(name='genus_out', s_filer=512, n_filer=24, 
            offset="(6,0,0)", to="(genus_mlp-east)", 
            width=2, height=14, depth=14, caption="Genus\\\\(24)"),
    to_connection("features", "genus_mlp"),
    to_connection("family_out", "genus_mlp"),  # Cascade from Family
    to_connection("genus_mlp", "genus_out"),
    
    # Species Head: MLP + Output
    to_ConvRelu(name='species_mlp', s_filer=1312, n_filer=1024, 
            offset="(0,-6,0)", to="(genus_mlp-south)", 
            width=3, height=24, depth=24, caption="1024\\\\Species\\\\MLP"),
    to_Conv(name='species_out', s_filer=1024, n_filer=82, 
            offset="(6,0,0)", to="(species_mlp-east)", 
            width=2.5, height=18, depth=18, caption="Species\\\\(82)"),
    to_connection("features", "species_mlp"),
    to_connection("genus_out", "species_mlp"),  # Cascade from Genus
    to_connection("species_mlp", "species_out"),
    
    # Additional cascade connections (from outputs to subsequent MLPs)
    to_connection("class_out", "family_mlp"),
    to_connection("class_out", "genus_mlp"),
    to_connection("class_out", "species_mlp"),
    to_connection("order_out", "genus_mlp"),
    to_connection("order_out", "species_mlp"),
    to_connection("family_out", "species_mlp"),
    
    to_end()
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()
