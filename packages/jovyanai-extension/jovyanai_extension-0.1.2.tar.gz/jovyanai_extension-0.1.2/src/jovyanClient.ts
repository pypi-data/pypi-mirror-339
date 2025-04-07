import { JovyanClient } from '@jovyan/client';
import { ISettingRegistry } from '@jupyterlab/settingregistry';

// Default settings
let backendUrl = 'wss://backend.jovyan-ai.com';
let authToken = '';

// Initialize with default values
let jovyanClientInstance = new JovyanClient(backendUrl, authToken, '');
let isConnected = false;

// Function to initialize settings from the registry
export const initializeClient = async (
  settingRegistry: ISettingRegistry
): Promise<void> => {
  try {
    const settings = await settingRegistry.load(
      '@jovyanai/labextension:plugin'
    );

    backendUrl = settings.get('backendUrl').composite as string;
    authToken = settings.get('authToken').composite as string;
  } catch (error) {
    console.error('Failed to load settings for @jovyanai/labextension:', error);
  }

  try {
    // Recreate the client instance with new settings
    console.debug('Recreating JovyanClient instance with new settings');
    jovyanClientInstance = new JovyanClient(backendUrl, authToken, '');
    await jovyanClientInstance.connect();
    const sessionId = await jovyanClientInstance.startSession();
    console.debug('Session ID:', sessionId);
    console.debug('JovyanClient instance created and connected');
    // We don't check isAuthenticated as it's private
    isConnected = true;
  } catch (error) {
    console.error('Failed to create JovyanClient instance:', error);
  }
};

export const getJovyanClient = async () => {
  if (!jovyanClientInstance) {
    throw new Error('JovyanClient instance not initialized');
  }
  if (!isConnected) {
    try {
      await jovyanClientInstance.connect();
      const sessionId = await jovyanClientInstance.startSession();
      console.debug('Session ID:', sessionId);
      console.debug('JovyanClient instance created and connected');
      isConnected = true;
    } catch (error) {
      console.error('Failed to create JovyanClient instance:', error);
    }
  }
  return jovyanClientInstance;
};

export const clientIsConnected = () => {
  return isConnected;
};
