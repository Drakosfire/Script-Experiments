import pickle

# Save a dictionary with a specific protocol
data = {'key': 'value'}
with open('test_pickle.pkl', 'wb') as f:
    pickle.dump(data, f, protocol=5)  # Try different protocol numbers

# Load the pickle file
with open('test_pickle.pkl', 'rb') as f:
    data_loaded = pickle.load(f)
print(data_loaded)
