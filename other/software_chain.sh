echo 'digraph G {
    Baseline_Generator[style=filled fillcolor="#6ab726" ];
    Raw_Level_Generator[style=filled fillcolor="#bc9ff2" ];
    Baseline_Generator->Raw_Level_Generator[label="Build Level XMLs" ];
    Raw_Level_Generator->NN[label="Generate samples for training"];
    NN[style=filled fillcolor="#5a55f4"];
    NN->Conture_Detector[label="Generate level images"];
    Conture_Detector[style=filled fillcolor="#96ffb9"];
    Conture_Detector->XML_Generator[label="Detect shapes and build XMLs"];
    XML_Generator[style=filled fillcolor="#f1f97c"];
    XML_Generator->{Physics_Test Naive_Agent_Test}[label="Hands on test In-Game"];
    Physics_Test[style=filled fillcolor="#fc9520"];
    Naive_Agent_Test[style=filled fillcolor="#fc9520"];
    {Physics_Test Naive_Agent_Test}->NN [label="feed result back"];
}' | dot -Tpng >../chain.png