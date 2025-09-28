import { useState } from 'react'
import { Save, TestTube, Key, Database, Bell } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'

export function Settings() {
  const [settings, setSettings] = useState({
    // API Settings
    cerebrasApiKey: '',
    defaultModel: '',
    maxTokens: 32768,
    temperature: 0.6,
    topP: 0.9,
    
    // Database Settings
    databaseUrl: '',
    redisUrl: '',
    
    // Application Settings
    appName: 'CrewAI Cerebras Platform',
    debugMode: true,
    logLevel: 'INFO',
    
    // Notification Settings
    emailNotifications: true,
    webhookUrl: '',
    slackWebhook: '',
  })

  const [isSaving, setIsSaving] = useState(false)
  const [isTesting, setIsTesting] = useState(false)

  const handleSave = async () => {
    setIsSaving(true)
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    setIsSaving(false)
    // Show success message
  }

  const handleTest = async () => {
    setIsTesting(true)
    // Simulate API test
    await new Promise(resolve => setTimeout(resolve, 2000))
    setIsTesting(false)
    // Show test result
  }

  const handleInputChange = (key: keyof typeof settings, value: unknown) => {
    setSettings(prev => ({ ...prev, [key]: value }))
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
          <p className="text-gray-600">Configure your CrewAI Cerebras Platform</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={handleTest} loading={isTesting}>
            <TestTube className="mr-2 h-4 w-4" />
            Test Connection
          </Button>
          <Button onClick={handleSave} loading={isSaving}>
            <Save className="mr-2 h-4 w-4" />
            Save Changes
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* API Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Key className="mr-2 h-5 w-5" />
              API Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="Cerebras API Key"
              type="password"
              value={settings.cerebrasApiKey}
              onChange={(e) => handleInputChange('cerebrasApiKey', e.target.value)}
              helper="Your Cerebras API key for model access"
            />
            
            <Input
              label="Default Model"
              value={settings.defaultModel}
              onChange={(e) => handleInputChange('defaultModel', e.target.value)}
              helper="Default model to use for new agents"
            />
            
            <div className="grid grid-cols-2 gap-4">
              <Input
                label="Max Tokens"
                type="number"
                value={settings.maxTokens}
                onChange={(e) => handleInputChange('maxTokens', parseInt(e.target.value))}
              />
              <Input
                label="Temperature"
                type="number"
                step="0.1"
                min="0"
                max="2"
                value={settings.temperature}
                onChange={(e) => handleInputChange('temperature', parseFloat(e.target.value))}
              />
            </div>
            
            <Input
              label="Top P"
              type="number"
              step="0.1"
              min="0"
              max="1"
              value={settings.topP}
              onChange={(e) => handleInputChange('topP', parseFloat(e.target.value))}
            />
          </CardContent>
        </Card>

        {/* Database Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Database className="mr-2 h-5 w-5" />
              Database Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="Database URL"
              type="url"
              value={settings.databaseUrl}
              onChange={(e) => handleInputChange('databaseUrl', e.target.value)}
              helper="PostgreSQL connection string"
            />
            
            <Input
              label="Redis URL"
              type="url"
              value={settings.redisUrl}
              onChange={(e) => handleInputChange('redisUrl', e.target.value)}
              helper="Redis connection string for caching"
            />
            
            <div className="flex items-center space-x-2">
              <Badge variant="success">Connected</Badge>
              <span className="text-sm text-gray-500">Database connection is active</span>
            </div>
          </CardContent>
        </Card>

        {/* Application Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Application Settings</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              label="Application Name"
              value={settings.appName}
              onChange={(e) => handleInputChange('appName', e.target.value)}
            />
            
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="debugMode"
                checked={settings.debugMode}
                onChange={(e) => handleInputChange('debugMode', e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <label htmlFor="debugMode" className="text-sm font-medium text-gray-700">
                Debug Mode
              </label>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Log Level
              </label>
              <select
                value={settings.logLevel}
                onChange={(e) => handleInputChange('logLevel', e.target.value)}
                className="input"
              >
                <option value="DEBUG">DEBUG</option>
                <option value="INFO">INFO</option>
                <option value="WARNING">WARNING</option>
                <option value="ERROR">ERROR</option>
              </select>
            </div>
          </CardContent>
        </Card>

        {/* Notification Settings */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <Bell className="mr-2 h-5 w-5" />
              Notification Settings
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="emailNotifications"
                checked={settings.emailNotifications}
                onChange={(e) => handleInputChange('emailNotifications', e.target.checked)}
                className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              <label htmlFor="emailNotifications" className="text-sm font-medium text-gray-700">
                Email Notifications
              </label>
            </div>
            
            <Input
              label="Webhook URL"
              type="url"
              value={settings.webhookUrl}
              onChange={(e) => handleInputChange('webhookUrl', e.target.value)}
              helper="URL for webhook notifications"
            />
            
            <Input
              label="Slack Webhook"
              type="url"
              value={settings.slackWebhook}
              onChange={(e) => handleInputChange('slackWebhook', e.target.value)}
              helper="Slack webhook URL for notifications"
            />
          </CardContent>
        </Card>
      </div>

      {/* System Information */}
      <Card>
        <CardHeader>
          <CardTitle>System Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div>
              <p className="text-sm text-gray-500">Version</p>
              <p className="text-sm font-medium">1.0.0</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Environment</p>
              <p className="text-sm font-medium">Development</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Uptime</p>
              <p className="text-sm font-medium">2 days, 14 hours</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Last Updated</p>
              <p className="text-sm font-medium">2024-01-15 10:30:00</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}