import onnxruntime as ort

class ChronousInferenceEngine:
    def __init__(self, onnx_model_path="models/isolation_forest.onnx"):
        self.session = ort.InferenceSession(onnx_model_path)

    def evaluate_health(self, features, z_score):
        # ONNX Inference
        inputs = {self.session.get_inputs()[0].name: features.astype(np.float32)}
        raw_score = self.session.run(None, inputs)[0][0]
        
        # Dual-Stage Decision Logic with False Alarm Suppression
        if raw_score < 0.48:
            stage = "HEALTHY"
            is_false_alarm = False
        elif raw_score < 0.58:
            stage = "WARNING"  # 48-72h Lead Time Window Starts
            is_false_alarm = False
        else:
            # Suppress false alarms if Kurtosis Z-Score didn't spike (transient speed noise)
            if z_score < 3.0:
                stage = "WARNING"  # Suppressed back to warning
                is_false_alarm = True
            else:
                stage = "CRITICAL"  # Confirmed structural damage
                is_false_alarm = False
                
        return {"score": raw_score, "stage": stage, "suppressed_false_alarm": is_false_alarm}