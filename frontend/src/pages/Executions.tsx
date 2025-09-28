import { useState } from 'react'
import { Search, MoreVertical, Play, Eye, Download, RefreshCw } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { formatRelativeTime, formatNumber } from '@/lib/utils'

// Mock data
const executions = [
  {
    id: 1,
    workflow: 'Content Generation Pipeline',
    status: 'completed',
    startedAt: '2024-01-15T10:30:00Z',
    completedAt: '2024-01-15T10:31:23Z',
    duration: '1m 23s',
    tasks: 4,
    completedTasks: 4,
    tokens: 1250,
    successRate: 100,
  },
  {
    id: 2,
    workflow: 'Data Analysis Workflow',
    status: 'running',
    startedAt: '2024-01-15T11:20:00Z',
    completedAt: null,
    duration: '0m 45s',
    tasks: 6,
    completedTasks: 2,
    tokens: 0,
    successRate: 0,
  },
  {
    id: 3,
    workflow: 'Research Assistant',
    status: 'failed',
    startedAt: '2024-01-15T09:15:00Z',
    completedAt: '2024-01-15T09:15:12Z',
    duration: '0m 12s',
    tasks: 3,
    completedTasks: 1,
    tokens: 0,
    successRate: 33,
  },
  {
    id: 4,
    workflow: 'Email Automation',
    status: 'completed',
    startedAt: '2024-01-15T08:45:00Z',
    completedAt: '2024-01-15T08:48:12Z',
    duration: '3m 12s',
    tasks: 5,
    completedTasks: 5,
    tokens: 2100,
    successRate: 100,
  },
  {
    id: 5,
    workflow: 'Content Generation Pipeline',
    status: 'completed',
    startedAt: '2024-01-14T16:30:00Z',
    completedAt: '2024-01-14T16:32:45Z',
    duration: '2m 45s',
    tasks: 4,
    completedTasks: 4,
    tokens: 1180,
    successRate: 100,
  },
  {
    id: 6,
    workflow: 'Data Analysis Workflow',
    status: 'cancelled',
    startedAt: '2024-01-14T14:20:00Z',
    completedAt: '2024-01-14T14:25:30Z',
    duration: '5m 30s',
    tasks: 6,
    completedTasks: 3,
    tokens: 0,
    successRate: 50,
  },
]

export function Executions() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  const filteredExecutions = executions.filter(execution => {
    const matchesSearch = execution.workflow.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || execution.status === filterStatus
    return matchesSearch && matchesStatus
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success'
      case 'running': return 'warning'
      case 'failed': return 'error'
      case 'cancelled': return 'secondary'
      case 'pending': return 'default'
      default: return 'secondary'
    }
  }

  // removed unused getProgressPercentage

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Executions</h1>
          <p className="text-gray-600">Monitor and manage workflow executions</p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline">
            <Download className="mr-2 h-4 w-4" />
            Export
          </Button>
          <Button variant="outline">
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:space-y-0 sm:space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Search executions..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>
            <div className="flex space-x-2">
              <Button
                variant={filterStatus === 'all' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('all')}
              >
                All
              </Button>
              <Button
                variant={filterStatus === 'completed' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('completed')}
              >
                Completed
              </Button>
              <Button
                variant={filterStatus === 'running' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('running')}
              >
                Running
              </Button>
              <Button
                variant={filterStatus === 'failed' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('failed')}
              >
                Failed
              </Button>
              <Button
                variant={filterStatus === 'cancelled' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('cancelled')}
              >
                Cancelled
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Executions List */}
      <div className="space-y-4">
        {filteredExecutions.map((execution) => (
          <Card key={execution.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <h3 className="text-lg font-medium text-gray-900">
                      {execution.workflow}
                    </h3>
                    <Badge variant={getStatusColor(execution.status)}>
                      {execution.status}
                    </Badge>
                    <span className="text-sm text-gray-500">
                      ID: #{execution.id}
                    </span>
                  </div>
                  
                  <div className="mt-2 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                    <div>
                      <p className="text-sm text-gray-500">Started</p>
                      <p className="text-sm font-medium">
                        {formatRelativeTime(execution.startedAt)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Duration</p>
                      <p className="text-sm font-medium">{execution.duration}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Tasks</p>
                      <p className="text-sm font-medium">
                        {execution.completedTasks}/{execution.tasks}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Tokens</p>
                      <p className="text-sm font-medium">
                        {formatNumber(execution.tokens)}
                      </p>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  {execution.status === 'running' && (
                    <div className="mt-4">
                      <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                        <span>Progress</span>
                        <span>{execution.successRate}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${execution.successRate}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Success Rate */}
                  {execution.status === 'completed' && (
                    <div className="mt-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-gray-500">Success Rate:</span>
                        <span className="text-sm font-medium text-success-600">
                          {execution.successRate}%
                        </span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-2 ml-6">
                  <Button variant="outline" size="sm">
                    <Eye className="mr-2 h-4 w-4" />
                    View
                  </Button>
                  {execution.status === 'running' && (
                    <Button variant="outline" size="sm">
                      <Play className="mr-2 h-4 w-4" />
                      Monitor
                    </Button>
                  )}
                  <Button variant="ghost" size="sm">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredExecutions.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="mx-auto max-w-md">
              <div className="mx-auto h-12 w-12 text-gray-400">
                <Search className="h-12 w-12" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">
                No executions found
              </h3>
              <p className="mt-2 text-sm text-gray-500">
                {searchTerm || filterStatus !== 'all'
                  ? 'Try adjusting your search or filter criteria.'
                  : 'No workflow executions have been run yet.'}
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}