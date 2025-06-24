// main.js - VaultSafe UI functionality

document.addEventListener('DOMContentLoaded', function () {
    // Decrypt button handler
    const decryptBtns = document.querySelectorAll('.btn-decrypt');
    decryptBtns.forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const decryptModal = document.getElementById('decryptModal');
        if (decryptModal) {
          decryptModal.style.display = 'block';
        } else {
          console.warn('decryptModal not found on this page.');
        }
      });
    });
  
    // Encrypt button handler
    const encryptBtns = document.querySelectorAll('.btn-encrypt');
    encryptBtns.forEach(btn => {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const encryptModal = document.getElementById('encryptModal');
        if (encryptModal) {
          encryptModal.style.display = 'block';
        } else {
          console.warn('encryptModal not found on this page.');
        }
      });
    });
  
    // Close modal buttons
    const closeButtons = document.querySelectorAll('.close-modal');
    closeButtons.forEach(button => {
      button.addEventListener('click', function () {
        const modal = this.closest('.modal');
        if (modal) {
          modal.style.display = 'none';
        }
      });
    });
  
    // Click outside modal to close
    window.addEventListener('click', function (e) {
      if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
      }
    });
  
    // Password key strength checker
    const keyInputs = document.querySelectorAll('input[type="password"]');
    keyInputs.forEach(input => {
      input.addEventListener('input', function () {
        checkKeyStrength(this);
      });
    });
  
    // Upload box drag-and-drop behavior
    const uploadBox = document.querySelector('.upload-box');
    if (uploadBox) {
      uploadBox.addEventListener('click', function () {
        document.getElementById('fileInput')?.click();
      });
  
      uploadBox.addEventListener('dragover', function (e) {
        e.preventDefault();
        this.style.borderColor = '#3498db';
        this.style.backgroundColor = 'rgba(52, 152, 219, 0.1)';
      });
  
      uploadBox.addEventListener('dragleave', function () {
        this.style.borderColor = '#ddd';
        this.style.backgroundColor = '';
      });
  
      uploadBox.addEventListener('drop', function (e) {
        e.preventDefault();
        this.style.borderColor = '#ddd';
        this.style.backgroundColor = '';
        console.log('Files dropped:', e.dataTransfer.files);
      });
    }
  });
  
  // Password strength logic
  function checkKeyStrength(input) {
    const value = input.value;
    const strength = value.length > 12 ? 'true' : 'false';
    input.setAttribute('data-strong', strength);
  
    const strengthMeter = input.nextElementSibling;
    if (strengthMeter && strengthMeter.classList.contains('key-strength')) {
      const meter = strengthMeter.querySelector('.key-strength-bar') || strengthMeter;
      let width = 0;
      let color = 'red';
  
      if (value.length >= 12) {
        width = 100;
        color = 'green';
      } else if (value.length >= 8) {
        width = 66;
        color = '#ffcc00';
      } else if (value.length >= 4) {
        width = 33;
        color = 'orange';
      }
  
      meter.style.width = `${width}%`;
      meter.style.backgroundColor = color;
    }
  }
  