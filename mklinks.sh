RESULTS_DIR="~/Programming/exact/results"
for datatype in coal c172 pa44 pa28; do
    mkdir -p $RESULTS_DIR/$datatype
    for nmut in 0 4 8; do
        mkdir -p $RESULTS_DIR/$datatype/m$nmut
        for ep in 1500 2000; do
            mkdir -p $RESULTS_DIR/$datatype/e$ep
            for ik in 1 2 3 4 5 6 7 8 9 10; do
                mkdir -p $RESULTS_DIR/$datatype/k$ik
                
                loc=$RESULTS_DIR/$datatype/bestGenome/num_island_kill_$ik/extinct_point_$ep/num_mutation_$nmut

                # Bin by num mutations
                ln -s $loc $RESULTS_DIR/$datatype/m$nmut/e${ep}k${ik}

                # Bin by extinction point
                ln -s $loc $RESULTS_DIR/$datatype/e$ep/m${nmut}k${ik}

                # Bin by n islands killed
                ln -s $loc $RESULTS_DIR/$datatype/k$ik/m${nmut}e$ep

            done
        end
    done
done
