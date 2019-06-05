

ARR_REQUEST=()
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00015)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00016)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00017)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00018)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00019)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00020)
ARR_REQUEST+=(HIG-RunIIFall17wmLHEGS-00021)

ARR_NEVENT=()
ARR_NEVENT+=(50000)
ARR_NEVENT+=(5000)
ARR_NEVENT+=(1000)

for req in ${ARR_REQUEST[@]};do
    for NEVENT in ${ARR_NEVENT[@]};do
	echo "@@Running "+${req}
    #(1)setup
	python run_MCM_setup_command.py --id ${req} --n ${NEVENT} 
    #(2)run
	pushd ${req}_${NEVENT}
	source setup.sh
	
	wget https://raw.githubusercontent.com/soarnsoar/python_tool/master/add_runtime.py
	echo 'cmsRun my_cfg.py' > myrun.sh
	python add_runtime.py myrun.sh
	source myrun.sh &> myrun.log&
	popd
    done
done