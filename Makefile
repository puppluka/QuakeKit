#    -------------------------------------------------------------------------------------------------------
#     ::::::::  :::    :::     :::     :::    ::: :::::::::: ::::    ::::      :::     :::    ::: :::::::::: 
#    :+:    :+: :+:    :+:   :+: :+:   :+:   :+:  :+:        +:+:+: :+:+:+   :+: :+:   :+:   :+:  :+:        
#    +:+    +:+ +:+    +:+  +:+   +:+  +:+  +:+   +:+        +:+ +:+:+ +:+  +:+   +:+  +:+  +:+   +:+        
#    +#+    +:+ +#+    +:+ +#++:++#++: +#++:++    +#++:++#   +#+  +:+  +#+ +#++:++#++: +#++:++    +#++:++#   
#    +#+  # +#+ +#+    +#+ +#+     +#+ +#+  +#+   +#+        +#+       +#+ +#+     +#+ +#+  +#+   +#+        
#    #+#   +#+  #+#    #+# #+#     #+# #+#   #+#  #+#        #+#       #+# #+#     #+# #+#   #+#  #+#        
#     ###### ### ########  ###     ### ###    ### ########## ###       ### ###     ### ###    ### ########## 
#    -------------------------------------------------------------------------------------------------------
#
#    version 0.10-beta
# ----------------------------------------------------------------
#	Variables
# ----------------------------------------------------------------
MAPS = ""

BSP_FLAGS = ""
LIGHT_FLAGS = "-extra4"
VIS_FLAGS = "-level 4"

WADPATH = $(shell realpath textures)

BINPATH = "_pak0"
# ----------------------------------------------------------------

.PHONY: all setup clean test deploy copy_demos

all: setup tree bincopy copy_demos qcc gfx-wad gfx progs map map-lits pack
	@echo "All tasks completed successfully."
	rm -rf $(BINPATH)

setup:
	@echo "Creating temp build directory..."
	@mkdir -pv $(BINPATH)
	
tree:
	@echo "Creating build tree..."
	@mkdir -pv $(BINPATH)/{gfx,maps,progs}
	rsync -av --exclude 'sound/_RAW' sound/ $(BINPATH)/sound

bincopy:
	cd $(BINPATH)
	
	@echo "Copying DOS Endscreens..."
	cp -r ../endscreen/*.bin .
	
	@echo "Writing Configuration Files..."
	python ../source/file_splitter.py ../config/files.dat
	
	@echo "Copying specified demo files..."
	

pack:
	@echo "Building master PAK file..."
	python source/makepak.py $(BINPATH) ./pak0.pak

gfx-wad:
	cd gfx-wad
	@echo "Creating GFX.WAD..."
	qpakman -pic *.png -o ../$(BINPATH)/gfx.wad

qcc:
	cd qcc-src
	@echo "Compiling game logic data..."
	qcc
	mv ../progs.dat ../$(BINPATH)/progs.dat

gfx:
	cd $(BINPATH)/gfx
	tga2pal ../../graphics/PALETTE/palette.tga
	@echo "Color palette successfully created."
	
	../../bin/linux/colorgen palette.lmp
	@echo "DOS Colormap generated successfully."
	
	@echo "Writing Proof-Of-Purchase data..."
	../../bin/linux/getpop
	
	@echo "Converting GFX files..."
	tga2lmp ../../graphics/*.tga
	mv ../../graphics/*.lmp .

progs:
	cd models
	
	cd spr_flame1
	tga2spr flame.qc
	
	cd ..
	@echo "Acquiring models and sprite progs..."
	find . -name '*.spr' -exec cp -prv '{}' '../$(BINPATH)/progs' ';'
	find . -name '*.mdl' -exec cp -prv '{}' '../$(BINPATH)/progs' ';'

clean:
	@echo "Cleaning up build files..."
	rm -rf $(BINPATH)
	rm pak0.pak

#This function reads config/files.dat for 'startdemo' values -- DO NOT ALTER FILEPATH
copy_demos:
	@grep "^startdemos" config/files.dat | \
	awk '{ for (i=2; i<=NF; i++) { \
	if ($$i ~ /^\/\//) { break; } \
	print $$i; } \
	}' | \
	while read demo_file; do \
	if [ -f "demos//$$demo_file.dem" ]; then \
	echo "Copying $$demo_file.dem..."; \
	cp "demos//$$demo_file.dem" "$(BINPATH)/"; \
	else \
	echo "Warning: $$demo_file.dem not found in demos/"; \
	fi; \
	done

maps: $(addsuffix .bsp, $(MAPS))

map-lits:
	@echo "Checking for .lit files..."
	find maps/ -name "*.lit" -exec mv -t $(BINPATH)/maps {} +
	echo "Check completed."

# ----------------------------------------------------------------

#MAP2BSP rule
$(BINPATH)/maps/%.bsp: maps/%.map
	@echo "--- Compiling $(basename $<) ---"
	@echo "Step 1/3: Running qbsp on $<..."
	qbsp -wadpath $(WADPATH) $< $@
	
	@echo "Step 2/3: Running light on $(basename $<).bsp..."
	light $(LIGHT_FLAGS) $@
	
	@echo "Step 3/3: Running vis on $(basename $<).bsp..."
	vis $(VIS_FLAGS) $@
	
	@echo "Map $(basename $<) successfully compiled!"
