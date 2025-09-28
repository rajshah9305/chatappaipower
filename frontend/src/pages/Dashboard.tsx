import React from 'react'
import { 
  Bot, 
  Workflow, 
  Activity, 
  Zap, 
  TrendingUp, 
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { formatNumber, formatRelativeTime } from '@/lib/utils'

// Mock data - in real app this would come from API
const stats = {
  totalAgents: 12,
  activeWorkflows: 8,
  totalExecutions: 1247,
  successRate: 94.2,
  avgExecutionTime: '2.3m',
  tokensUsed: 1250000,
}

const recentExecutions = [
  {
    id: 1,
    workflow: 'Content Generation Pipeline',
    status: 'completed',
    duration: '1m 23s',
    tokens: 1250,
    completedAt: '2024-01-15T10:30:00Z',
  },
  {
    id: 2,
    workflow: 'Data Analysis Workflow',
    status: 'running',
    duration: '0m 45s',
    tokens: 0,
    completedAt: null,
  },
  {
    id: 3,
    workflow: 'Research Assistant',
    status: 'failed',
    duration: '0m 12s',
    tokens: 0,
    completedAt: '2024-01-15T09:15:00Z',
  },
  {
    id: 4,
    workflow: 'Email Automation',
    status: 'completed',
    duration: '3m 12s',
    tokens: 2100,
    completedAt: '2024-01-15T08:45:00Z',
  },
]

const topAgents = [
  { name: 'Researcher', executions: 245, successRate: 96.3 },
  { name: 'Writer', executions: 198, successRate: 94.7 },
  { name: 'Analyst', executions: 156, successRate: 92.1 },
  { name: 'Coordinator', executions: 134, successRate: 98.5 },
]

export function Dashboard() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Welcome to CrewAI Cerebras Platform</p>
        </div>
        <Button className="btn-primary">
          <Zap className="mr-2 h-4 w-4" />
          Create Workflow
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Bot className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Agents</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {formatNumber(stats.totalAgents)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Workflow className="h-8 w-8 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Workflows</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {formatNumber(stats.activeWorkflows)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Activity className="h-8 w-8 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Executions</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {formatNumber(stats.totalExecutions)}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <TrendingUp className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Success Rate</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {stats.successRate}%
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Executions */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Executions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentExecutions.map((execution) => (
                <div
                  key={execution.id}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                >
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <h4 className="text-sm font-medium text-gray-900">
                        {execution.workflow}
                      </h4>
                      <Badge
                        variant={
                          execution.status === 'completed'
                            ? 'success'
                            : execution.status === 'running'
                            ? 'warning'
                            : 'error'
                        }
                      >
                        {execution.status}
                      </Badge>
                    </div>
                    <div className="mt-1 flex items-center space-x-4 text-sm text-gray-500">
                      <span className="flex items-center">
                        <Clock className="mr-1 h-3 w-3" />
                        {execution.duration}
                      </span>
                      {execution.tokens > 0 && (
                        <span>{formatNumber(execution.tokens)} tokens</span>
                      )}
                      {execution.completedAt && (
                        <span>{formatRelativeTime(execution.completedAt)}</span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    {execution.status === 'completed' && (
                      <CheckCircle className="h-5 w-5 text-success-500" />
                    )}
                    {execution.status === 'running' && (
                      <div className="h-5 w-5 animate-spin rounded-full border-2 border-primary-600 border-t-transparent" />
                    )}
                    {execution.status === 'failed' && (
                      <AlertCircle className="h-5 w-5 text-error-500" />
                    )}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Top Agents */}
        <Card>
          <CardHeader>
            <CardTitle>Top Performing Agents</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topAgents.map((agent, index) => (
                <div
                  key={agent.name}
                  className="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
                >
                  <div className="flex items-center space-x-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-primary-600 font-medium text-sm">
                      {index + 1}
                    </div>
                    <div>
                      <h4 className="text-sm font-medium text-gray-900">
                        {agent.name}
                      </h4>
                      <p className="text-sm text-gray-500">
                        {formatNumber(agent.executions)} executions
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-gray-900">
                      {agent.successRate}%
                    </p>
                    <p className="text-xs text-gray-500">success rate</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Bot className="h-6 w-6" />
              <span>Create Agent</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Workflow className="h-6 w-6" />
              <span>New Workflow</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Activity className="h-6 w-6" />
              <span>View Executions</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Zap className="h-6 w-6" />
              <span>Test Agent</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}