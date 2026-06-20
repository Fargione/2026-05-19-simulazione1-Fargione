from model.model import Model

mdl = Model()
print(f"Nodi esistenti: {mdl.getNumNodes()} e archi esistenti: {mdl.getNumEdges()}")

mdl.buildGrafo("Rock")
print(f"Nodi esistenti: {mdl.getNumNodes()} e archi esistenti: {mdl.getNumEdges()}")

mdl.drawGraph()