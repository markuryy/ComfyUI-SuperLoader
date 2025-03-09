import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

// Simple object to store serialized workflow
const initialGraphToPromptSerializedWorkflow = {
  getNodeFromInitialGraphToPromptSerializedWorkflowBecauseComfyUIBrokeStuff: function(node) {
    if (!this.workflow || !this.workflow.nodes) return null;
    return this.workflow.nodes.find(n => n.id === node.id) || null;
  },
  workflow: null
};

// Hook into graph serialization
const graphSerialize = LGraph.prototype.serialize;
LGraph.prototype.serialize = function() {
  const response = graphSerialize.apply(this, [...arguments]);
  initialGraphToPromptSerializedWorkflow.workflow = response;
  return response;
};

// Empty function to satisfy the call
function addConnectionLayoutSupport(nodeType, app, options) {}

app.registerExtension({
  name: "superloader.string.preview",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "Display String" || nodeData.name === "Display String Multiline") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function() {
        onNodeCreated ? onNodeCreated.apply(this, []) : undefined;
        this.showValueWidget = ComfyWidgets["STRING"](this, "output", ["STRING", { multiline: true }], app).widget;
        this.showValueWidget.inputEl.readOnly = true;
        this.showValueWidget.serializeValue = async (node, index) => {
          const n = initialGraphToPromptSerializedWorkflow.getNodeFromInitialGraphToPromptSerializedWorkflowBecauseComfyUIBrokeStuff(node);
          if (n) {
            n.widgets_values[index] = "";
          } else {
            console.warn("No serialized node found in workflow. May be attributed to " +
              "https://github.com/comfyanonymous/ComfyUI/issues/2193");
          }
          return "";
        };
      };
      
      addConnectionLayoutSupport(nodeType, app, [["Left"], ["Right"]]);
      
      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function(message) {
        onExecuted ? onExecuted.apply(this, [message]) : undefined;
        this.showValueWidget.value = message.text[0];
      };
    }
  }
});
