"""Small, reproducible educational experiment. See README for limitations."""
import json
from pathlib import Path
import numpy as np

def save(result, output):
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result

from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score, confusion_matrix

def normal(rng,n):
    a=rng.normal(size=n); b=.6*a+rng.normal(0,.65,n)
    return np.column_stack([a,b,rng.normal(size=n)])
def run(output="results.json"):
    rng=np.random.default_rng(42)
    train=normal(rng,800); validation=normal(rng,200)
    test=np.vstack([normal(rng,500),rng.normal(3,1,(60,3))]); y=np.r_[np.zeros(500,dtype=int),np.ones(60,dtype=int)]
    model=IsolationForest(n_estimators=150,random_state=42,n_jobs=1).fit(train)
    threshold=float(np.quantile(-model.score_samples(validation),.95))
    scores=-model.score_samples(test); pred=(scores>threshold).astype(int)
    return save({"seed":42,"train_normal_rows":800,"validation_normal_rows":200,"test_normal_rows":500,"test_anomaly_rows":60,"threshold_source":"95th percentile of normal validation anomaly scores","threshold":threshold,"precision":float(precision_score(y,pred,zero_division=0)),"recall":float(recall_score(y,pred)),"f1":float(f1_score(y,pred)),"average_precision":float(average_precision_score(y,scores)),"false_positive_rate":float(np.mean(pred[y==0])),"confusion_matrix":confusion_matrix(y,pred).tolist()},output)

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
