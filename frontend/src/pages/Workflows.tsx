import { useState } from 'react'
import { Plus, Search, MoreVertical, Play, Edit, Trash2, Eye } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { formatRelativeTime } from '@/lib/utils'

// Mock data
const workflows = [
  {
    id: 1,
    name: 'Content Generation Pipeline',
    description: 'Automated content creation workflow using multiple AI agents',
    type: 'linear',
    status: 'active',
    executions: 45,
    successRate: 94.2,
    lastExecuted: '2024-01-15T10:30:00Z',
    tasks: 4,
    agents: ['Researcher', 'Writer', 'Editor', 'Publisher'],
  },
  {
    id: 2,
    name: 'Data Analysis Workflow',
    description: 'Comprehensive data analysis and reporting pipeline',
    type: 'parallel',
    status: 'running',
    executions: 23,
    successRate: 87.5,
    lastExecuted: '2024-01-15T11:20:00Z',
    tasks: 6,
    agents: ['Data Collector', 'Analyst', 'Visualizer', 'Reporter'],
  },
  {
    id: 3,
    name: 'Research Assistant',
    description: 'Automated research and information gathering workflow',
    type: 'conditional',
    status: 'paused',
    executions: 67,
    successRate: 91.3,
    lastExecuted: '2024-01-14T16:45:00Z',
    tasks: 3,
    agents: ['Researcher', 'Summarizer', 'Fact Checker'],
  },
  {
    id: 4,
    name: 'Email Automation',
    description: 'Automated email processing and response workflow',
    type: 'linear',
    status: 'active',
    executions: 89,
    successRate: 96.8,
    lastExecuted: '2024-01-15T08:45:00Z',
    tasks: 5,
    agents: ['Email Parser', 'Classifier', 'Responder', 'Scheduler'],
  },
]

export function Workflows() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  const [filterType, setFilterType] = useState('all')

  const filteredWorkflows = workflows.filter(workflow => {
    const matchesSearch = workflow.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         workflow.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = filterStatus === 'all' || workflow.status === filterStatus
    const matchesType = filterType === 'all' || workflow.type === filterType
    return matchesSearch && matchesStatus && matchesType
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'success'
      case 'running': return 'warning'
      case 'paused': return 'secondary'
      case 'completed': return 'default'
      case 'failed': return 'error'
      default: return 'secondary'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'linear': return 'primary'
      case 'parallel': return 'success'
      case 'conditional': return 'warning'
      case 'loop': return 'error'
      default: return 'secondary'
    }
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Workflows</h1>
          <p className="text-gray-600">Design and manage your AI agent workflows</p>
        </div>
        <Button className="btn-primary">
          <Plus className="mr-2 h-4 w-4" />
          Create Workflow
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col space-y-4 sm:flex-row sm:items-center sm:space-y-0 sm:space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Search workflows..."
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
                All Status
              </Button>
              <Button
                variant={filterStatus === 'active' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('active')}
              >
                Active
              </Button>
              <Button
                variant={filterStatus === 'running' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('running')}
              >
                Running
              </Button>
              <Button
                variant={filterStatus === 'paused' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('paused')}
              >
                Paused
              </Button>
            </div>
            <div className="flex space-x-2">
              <Button
                variant={filterType === 'all' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterType('all')}
              >
                All Types
              </Button>
              <Button
                variant={filterType === 'linear' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterType('linear')}
              >
                Linear
              </Button>
              <Button
                variant={filterType === 'parallel' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterType('parallel')}
              >
                Parallel
              </Button>
              <Button
                variant={filterType === 'conditional' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterType('conditional')}
              >
                Conditional
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Workflows Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredWorkflows.map((workflow) => (
          <Card key={workflow.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <CardTitle className="text-lg">{workflow.name}</CardTitle>
                  <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                    {workflow.description}
                  </p>
                </div>
                <div className="flex items-center space-x-2 ml-4">
                  <Badge variant={getStatusColor(workflow.status)}>
                    {workflow.status}
                  </Badge>
                  <Button variant="ghost" size="sm">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <Badge variant={getTypeColor(workflow.type)}>
                    {workflow.type}
                  </Badge>
                  <div className="text-sm text-gray-500">
                    {workflow.tasks} tasks
                  </div>
                </div>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Executions:</span>
                    <span className="font-medium">{workflow.executions}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Success Rate:</span>
                    <span className="font-medium text-success-600">
                      {workflow.successRate}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Last Executed:</span>
                    <span className="font-medium">
                      {formatRelativeTime(workflow.lastExecuted)}
                    </span>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-sm font-medium text-gray-700">Agents:</p>
                  <div className="flex flex-wrap gap-1">
                    {workflow.agents.map((agent) => (
                      <Badge key={agent} variant="outline" size="sm">
                        {agent}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="flex space-x-2 pt-4">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Eye className="mr-2 h-4 w-4" />
                    View
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Play className="mr-2 h-4 w-4" />
                    Run
                  </Button>
                  <Button variant="outline" size="sm">
                    <Edit className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Empty State */}
      {filteredWorkflows.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="mx-auto max-w-md">
              <div className="mx-auto h-12 w-12 text-gray-400">
                <Search className="h-12 w-12" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">
                No workflows found
              </h3>
              <p className="mt-2 text-sm text-gray-500">
                {searchTerm || filterStatus !== 'all' || filterType !== 'all'
                  ? 'Try adjusting your search or filter criteria.'
                  : 'Get started by creating your first workflow.'}
              </p>
              {!searchTerm && filterStatus === 'all' && filterType === 'all' && (
                <div className="mt-6">
                  <Button className="btn-primary">
                    <Plus className="mr-2 h-4 w-4" />
                    Create Workflow
                  </Button>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}