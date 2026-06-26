import os
import torch
import yaml

from torch import nn
from final_project.src.models.simple_cnn import cnnModel

EPOCHS = 30
DEVICE = "cuda"
DB_PATH = "db/"
MODELS_PATH = "src/models"
CONFIG_PATH = os.path.join(MODELS_PATH, "topology.yaml")

def load_configs(config_path: str):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config

def trainingPipeline(device, db_path, configs):
    from final_project.src.utils.load_data import getTrainingDataLoaders
    train_loader, val_loader, test_loader = getTrainingDataLoaders(db_path)

    simple_configs = configs['simple_cnn']
    complete_configs = configs['complex_cnn']

    simpleModel = cnnModel(
        device=device,
        filters_list=simple_configs['filters_list'],
        dropout=simple_configs['dropout'],
        batch_norm=simple_configs['batch_norm'],
        GAP=simple_configs['GAP'],
        best_model_path=simple_configs['best_model_path']
    )

    completeModel = cnnModel(
        device=device,
        filters_list=complete_configs['filters_list'],
        dropout=complete_configs['dropout'],
        batch_norm=complete_configs['batch_norm'],
        GAP=complete_configs['GAP'],
        best_model_path=complete_configs['best_model_path']
    )

    import torch.optim as optim
    optimizer_simple = optim.Adam(simpleModel.model.parameters(), lr=0.001)
    optimizer_complete = optim.Adam(completeModel.model.parameters(), lr=0.0001)
    loss_fn = nn.CrossEntropyLoss()
    num_epochs = EPOCHS

    best_simple_val_loss = float('inf')
    best_complete_val_loss = float('inf')
    for epoch in range(num_epochs):
        simpleModel.trainModel(train_loader, loss_fn, optimizer_simple)
        completeModel.trainModel(train_loader, loss_fn, optimizer_complete)

        simpleModel.validateModel(val_loader, loss_fn)
        completeModel.validateModel(val_loader, loss_fn)

        if simpleModel.val_loss[-1] < best_simple_val_loss:
            best_simple_val_loss = simpleModel.val_loss[-1]
            simpleModel.saveCeckpoint()
            print(f"Epoch {epoch+1}: Melhor modelo (simples) salvo! (Val Loss: {best_simple_val_loss:.4f})")

        if completeModel.val_loss[-1] < best_complete_val_loss:
            best_complete_val_loss = completeModel.val_loss[-1]
            completeModel.saveCheckpoint()
            print(f"Epoch {epoch+1}: Melhor modelo (completo) salvo! (Val Loss: {best_complete_val_loss:.4f})")

        if (epoch+1) % 5 == 0:
            print(f"Epoch {epoch+1}/{EPOCHS} | Simple Train Loss: {simpleModel.train_loss[epoch]:.4f} | Simple Val Loss: {simpleModel.val_loss[epoch]:.4f}")
            print(f"Epoch {epoch+1}/{EPOCHS} | Complete Train Loss: {completeModel.train_loss[epoch]:.4f} | Complete Val Loss: {completeModel.val_loss[epoch]:.4f}")

    from final_project.src.utils.view_loss import plotLosses, plotCMatrix
    plotLosses(
        "Modelo Simples",
        simpleModel.train_loss,
        simpleModel.val_loss,
        "Erro de treino",
        "Erro de validação",
        EPOCHS,
        "assets/Simple_CNN_Losses.png"
    )

    plotLosses(
        "Modelo Completo",
        completeModel.train_loss,
        completeModel.val_loss,
        "Erro de treino",
        "Erro de validação",
        EPOCHS,
        "assets/Complete_CNN_Losses.png"
    )

    simpleModel.model.load_state_dict(torch.load(simple_configs['best_model_path']))
    simpleModel.testModel(test_loader)
    print(f"--- Relatório Final (Modelo Simples) ---")
    print(f"Acurácia (Accuracy):   {simpleModel.acc*100:.2f}%")
    print(f"Precisão (Precision):  {simpleModel.prec*100:.2f}%")
    print(f"Sensibilidade (Recall):{simpleModel.rec*100:.2f}%")
    print(f"F1 Score:              {simpleModel.f1*100:.2f}%")

    completeModel.model.load_state_dict(torch.load(complete_configs['best_model_path']))
    completeModel.testModel(test_loader)
    print(f"--- Relatório Final (Modelo Completo) ---")
    print(f"Acurácia (Accuracy):   {completeModel.acc*100:.2f}%")
    print(f"Precisão (Precision):  {completeModel.prec*100:.2f}%")
    print(f"Sensibilidade (Recall):{completeModel.rec*100:.2f}%")
    print(f"F1 Score:              {completeModel.f1*100:.2f}%")

    plotCMatrix(
        simpleModel.test_class,
        simpleModel.predicted_class,
        ['Normal', 'Pneumonia'],
        "assets/Simple_CNN_ConfusionMatrix.png"
    )

    plotCMatrix(
        completeModel.test_class,
        completeModel.predicted_class,
        ['Normal', 'Pneumonia'],
        "assets/Complete_CNN_ConfusionMatrix.png"
    )

def predictionPipeline(device, db_path, model_path):
    from final_project.src.utils.load_data import getSampleData

    simple_configs = configs['simple_cnn']
    complete_configs = configs['complex_cnn']
    
    simpleModel = cnnModel(
        device=device,
        filters_list=simple_configs['filters_list'],
        dropout=simple_configs['dropout'],
        batch_norm=simple_configs['batch_norm'],
        GAP=simple_configs['GAP'],
        best_model_path=simple_configs['best_model_path']
    )

    completeModel = cnnModel(
        device=device,
        filters_list=complete_configs['filters_list'],
        dropout=complete_configs['dropout'],
        batch_norm=complete_configs['batch_norm'],
        GAP=complete_configs['GAP'],
        best_model_path=complete_configs['best_model_path']
    )

    simpleModel.model.load_state_dict(torch.load(simple_configs['best_model_path']))
    completeModel.model.load_state_dict(torch.load(complete_configs['best_model_path']))

if __name__ == "__main__":
    os.makedirs("src/models", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    configs = load_configs()
    predictionPipeline(DEVICE, DB_PATH)