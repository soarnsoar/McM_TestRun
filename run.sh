

ARR_REQUEST=()
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00015)


for req in ${ARR_REQUEST[@]};do
    python run_MCM_setup_command.py --id ${req} --n 50000 
done