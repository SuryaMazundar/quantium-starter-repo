import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dash import Dash

def test_app_creation():
    """Test that the app can be created successfully"""
    try:
        # Try to import and create the app
        from app import create_app
        app = create_app()
        
        # Check app is instance of Dash
        assert isinstance(app, Dash), "App should be an instance of Dash"
        
        # Check app has layout
        assert hasattr(app, 'layout'), "App should have a layout"
        assert app.layout is not None, "App layout should not be None"
        
        print("✓ Test 1 passed: App can be created successfully")
        return True
    except Exception as e:
        print(f"✗ Test 1 failed: {e}")
        return False

def test_layout_components():
    """Test that key components exist in the layout"""
    try:
        from app import create_app
        app = create_app()
        
        # Convert layout to string for inspection
        layout_str = str(app.layout).lower()
        
        # Check for header
        assert "pink morsel sales visualizer" in layout_str, \
            "Header should contain 'Pink Morsel Sales Visualizer'"
        
        # Check for graph component
        assert "sales_graph" in layout_str, \
            "Layout should contain 'sales_graph' component"
        
        # Check for region selector
        assert "region_selector" in layout_str, \
            "Layout should contain 'region_selector' component"
        
        # Check for region options
        assert "all regions" in layout_str or "all" in layout_str, \
            "Layout should contain 'All' or 'All Regions' option"
        
        print("✓ Test 2 passed: Key layout components are present")
        return True
    except Exception as e:
        print(f"✗ Test 2 failed: {e}")
        return False

def test_data_loading():
    """Test that data can be loaded successfully"""
    try:
        from app import load_data
        
        data = load_data()
        
        # Check data is not empty
        assert len(data) > 0, "Loaded data should not be empty"
        
        # Check required columns exist
        required_columns = ['date', 'sales']
        for col in required_columns:
            assert col in data.columns, f"Data should contain '{col}' column"
        
        print("✓ Test 3 passed: Data loads successfully")
        return True
    except Exception as e:
        print(f"✗ Test 3 failed: {e}")
        return False

def run_all_tests():
    """Run all tests and return exit code"""
    print("=" * 60)
    print("Running CI Tests for Pink Morsel Sales Visualizer")
    print("=" * 60)
    
    tests = [
        ("App Creation", test_app_creation),
        ("Layout Components", test_layout_components),
        ("Data Loading", test_data_loading)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        print("-" * 40)
        
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("All tests passed!")
        return 0  # Exit code 0 for success
    else:
        print("Some tests failed.")
        return 1  # Exit code 1 for failure

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)