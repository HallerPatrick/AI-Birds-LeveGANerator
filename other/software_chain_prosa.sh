echo 'digraph G {
    "Baseline Generator"[style=filled fillcolor="#6ab726" ];
    "Raw Level Generator"[style=filled fillcolor="#bc9ff2" ];
    "Baseline Generator"->"Raw Level Generator"[label="Generate levels in XML format" ];
    "Raw Level Generator"->"Neural Network (GAN)"[label="Generate samples for training in image format"];
    "Neural Network (GAN)"[style=filled fillcolor="#5a55f4"];
    "Neural Network (GAN)"->"Conture Detector"[label="Generate level images"];
    "Conture Detector"[style=filled fillcolor="#96ffb9"];
    "Conture Detector"->"XML Generator"[label="Detect shapes and build XMLs"];
    "XML Generator"[style=filled fillcolor="#f1f97c"];
    "XML Generator"->{"Physics Test" "Naive Agent Test"}[label="Hands on test In-Game"];
    "Physics Test"[style=filled fillcolor="#fc9520"];
    "Naive Agent Test"[style=filled fillcolor="#fc9520"];
    {"Physics Test" "Naive Agent Test"}->"Neural Network (GAN)" [label="Feeding results back"];
}' | dot -Tpng > prosa.png