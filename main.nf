nextflow.enable.dsl=2

process prepareData {
    tag 'prepare-data'
    input:
    path _data

    output:
    path 'data/train.csv', emit: train
    path 'data/val.csv', emit: val
    path 'data/test.csv', emit: test

    script:
    """
    echo \$PATH
    ls -l /workspace/work
    prepare_data.py --input $_data --train data/train.csv --val data/val.csv --test data/test.csv
    """
}

process trainInitialModel {
    tag 'train-initial-model'
	queue = 'hpc'
    input:
    path train
    path val

    output:
    path 'models/initial_model.pkl', emit: initialmodel
    path 'models/initial_model_results.txt'

    script:
    """
    python3 $projectDir/train.py --train $train --val $val --params '{}' --output models/initial_model.pkl
    """
}

process evaluateInitialModel {
    tag 'evaluate-initial-model'
    input:
    path initialmodel
    path test

    output:
    path 'models/initial_evaluation.txt'

    script:
    """
    python3 $projectDir/evaluate.py --model $initialmodel --input $test --output models/initial_evaluation.txt
    """
}

process hyperparameterTuning {
    tag 'hyperparameter-tuning'
    input:
    path train
    path val
    each param

    output:
    path "models/model_${param.replaceAll(/[^a-zA-Z0-9]/, '_')}.pkl"
    path "models/model_${param.replaceAll(/[^a-zA-Z0-9]/, '_')}_results.txt", emit: results

    script:
    """
    python3 $projectDir/train.py --train $train --val $val --params '${param.replaceAll(/'/, "\\'")}' --output models/model_${param.replaceAll(/[^a-zA-Z0-9]/, '_')}.pkl
    """
}

process evaluateTuningResults {
    tag 'evaluate-tuning-results'
    input:
	val ready
    path _modeloutputs

    output:
    path 'models/best_model_params.txt'

    script:
    """
    python3 $projectDir/evaluate_tuning.py --results_dir $_modeloutputs --output models/best_model_params.txt
    """
}

workflow {
    _data = Channel.fromPath("${projectDir}/${params.input_file}")
    _modeloutputs = Channel.fromPath("${projectDir}/models/")

    prepareData(_data)
    trainInitialModel(prepareData.out.train, prepareData.out.val)
    evaluateInitialModel(trainInitialModel.out.initialmodel, prepareData.out.test)
	hyperparameterTuning(prepareData.out.train, prepareData.out.val, params.hyperparams)
    evaluateTuningResults(hyperparameterTuning.out.results, _modeloutputs)
}