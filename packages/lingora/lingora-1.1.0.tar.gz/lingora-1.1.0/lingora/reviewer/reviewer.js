function translationReviewer() {
    return {
        translations: {},
        notification: {
            show: false,
            message: ''
        },
        
        async loadTranslations() {
            try {
                const response = await fetch('/api/translations');
                const data = await response.json();
                
                // Process translations into a more usable format
                const processed = {};
                
                Object.entries(data.source).forEach(([file, sourceData]) => {
                    processed[file] = {};
                    const targetData = data.target[file] || {};
                    
                    this.processObject(sourceData, targetData, processed[file]);
                });
                
                this.translations = processed;
            } catch (error) {
                console.error('Error loading translations:', error);
                this.showNotification('Error loading translations', 'is-danger');
            }
        },
        
        processObject(source, target, output, prefix = '') {
            Object.entries(source).forEach(([key, value]) => {
                const fullKey = prefix ? `${prefix}.${key}` : key;
                
                if (typeof value === 'object' && value !== null) {
                    this.processObject(value, target[key] || {}, output, fullKey);
                } else {
                    output[fullKey] = {
                        source: value,
                        target: target[key] || '',
                        editing: false
                    };
                }
            });
        },
        
        toggleEdit(file, key) {
            if (this.translations[file][key].editing) {
                this.saveTranslation(file, key);
            } else {
                this.translations[file][key].editing = true;
            }
        },
        
        async saveTranslation(file, key) {
            try {
                const response = await fetch('/api/translations', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        file,
                        key,
                        value: this.translations[file][key].target
                    })
                });
                
                if (!response.ok) throw new Error('Failed to save translation');
                
                this.translations[file][key].editing = false;
                this.showNotification(`Updated translation in ${file} for key: ${key}`);
            } catch (error) {
                console.error('Error saving translation:', error);
                this.showNotification('Error saving translation', 'is-danger');
            }
        },
        
        approveTranslation(file, key) {
            delete this.translations[file][key];
            if (Object.keys(this.translations[file]).length === 0) {
                delete this.translations[file];
            }
        },
        
        showNotification(message, type = 'is-success') {
            this.notification.message = message;
            this.notification.show = true;
            setTimeout(() => {
                this.notification.show = false;
            }, 5000);
        }
    };
} 