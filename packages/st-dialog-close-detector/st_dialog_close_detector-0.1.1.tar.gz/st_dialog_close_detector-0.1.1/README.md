# Streamlit Dialog Close Detector

> Automatically rerun Streamlit app when a dialog is closed

## The Problem

As of Streamlit v1.44, the official `st.dialog` component cannot trigger an app rerun when users close the dialog by either clicking outside the dialog or pressing the escape key.

While we can add a button inside the dialog to trigger a rerun, it would be more convenient if all widget states inside the dialog were automatically reflected in the main app when the dialog closes - meaning the app would automatically rerun upon dialog closure.

## The Solution

This component injects JavaScript to detect when a dialog is closed and updates the value of a custom component. This value update automatically triggers an app rerun.

## Usage

### Installation

```bash
uv add st-dialog-close-detector
```

### Implementation

Add the component **anywhere** in your Streamlit app:

```python
from st_dialog_close_detector import dialog_close_detector

dialog_close_detector()
```
