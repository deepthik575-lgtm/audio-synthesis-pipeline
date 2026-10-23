import os

# The folder inside your project
TEST_DIR = "generated_audio"

print(f"--- Checking path: {os.getcwd()} ---")

try:
    # 1. Try to create the folder
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
        print(f"✅ Created folder: {TEST_DIR}")
    else:
        print(f"ℹ️ Folder '{TEST_DIR}' already exists.")
    
    # 2. Try to write a file
    test_file = os.path.join(TEST_DIR, "test_permission.txt")
    with open(test_file, "w") as f:
        f.write("Windows has write access!")
    
    print("✅ SUCCESS: Successfully wrote to the folder.")
    
    # 3. Clean up
    os.remove(test_file)
    print("✅ SUCCESS: Successfully deleted the test file.")
    print("\nCONCLUSION: Your permissions are perfect. You can proceed safely.")

except Exception as e:
    print(f"\n❌ ERROR: Write access denied.")
    print(f"Reason: {e}")
    print("\nACTION: Right-click the folder -> Properties -> Uncheck 'Read-only'.")