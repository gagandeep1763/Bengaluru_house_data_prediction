import pickle
import pandas as pd
import numpy as np

print("🔍 Examining RidgeModel.pki file...")
print("=" * 50)

try:
    # Try to load the model
    with open("RidgeModel.pki", 'rb') as f:
        model = pickle.load(f)
    
    print("✅ Model loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Model: {model}")
    
    # Check if it's a pipeline
    if hasattr(model, 'steps'):
        print("\n📋 Pipeline Steps:")
        for i, (name, step) in enumerate(model.steps):
            print(f"  {i+1}. {name}: {type(step)}")
    
    # Check if it's a single estimator
    if hasattr(model, 'predict'):
        print("\n🎯 Model has predict method")
        
        # Try to get feature names if available
        if hasattr(model, 'feature_names_in_'):
            print(f"Feature names: {model.feature_names_in_}")
        
        if hasattr(model, 'coef_'):
            print(f"Number of coefficients: {len(model.coef_)}")
            print(f"First few coefficients: {model.coef_[:5]}")
    
    # Check for any other attributes
    print("\n🔧 Model attributes:")
    for attr in dir(model):
        if not attr.startswith('_'):
            try:
                value = getattr(model, attr)
                if not callable(value):
                    print(f"  {attr}: {type(value)}")
            except:
                pass
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    print(f"Error type: {type(e)}")
    
    # Try to get more details about the error
    import traceback
    print("\n📋 Full error traceback:")
    traceback.print_exc()

print("\n" + "=" * 50)
print("🔍 Model examination complete!")
