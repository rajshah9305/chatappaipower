import React, { useState } from 'react'
import { Plus, Search, Filter, MoreVertical, Play, Edit, Trash2 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Badge } from '@/components/ui/Badge'
import { formatRelativeTime } from '@/lib/utils'

// Mock data
const agents = [
  {
    id: 1,
    name: 'Researcher',
    role: 'Research Specialist',
    goal: 'Gather and analyze information from various sources',
    model: 'llama-4-maverick-17b-128e-instruct',
    status: 'active',
    executions: 245,
    successRate: 96.3,
    lastUsed: '2024-01-15T10:30:00Z',
    capabilities: ['Web Search', 'Data Analysis', 'Report Generation'],
  },
  {
    id: 2,
    name: 'Writer',
    role: 'Content Creator',
    goal: 'Create high-quality written content based on research and requirements',
    model: 'llama-4-maverick-17b-128e-instruct',
    status: 'active',
    executions: 198,
    successRate: 94.7,
    lastUsed: '2024-01-15T09:15:00Z',
    capabilities: ['Content Writing', 'Editing', 'SEO Optimization'],
  },
  {
    id: 3,
    name: 'Analyst',
    role: 'Data Analyst',
    goal: 'Analyze data and provide insights and recommendations',
    model: 'llama-4-maverick-17b-128e-instruct',
    status: 'inactive',
    executions: 156,
    successRate: 92.1,
    lastUsed: '2024-01-14T16:45:00Z',
    capabilities: ['Statistical Analysis', 'Visualization', 'Trend Analysis'],
  },
  {
    id: 4,
    name: 'Coordinator',
    role: 'Project Coordinator',
    goal: 'Coordinate tasks and manage workflow execution',
    model: 'llama-4-maverick-17b-128e-instruct',
    status: 'active',
    executions: 134,
    successRate: 98.5,
    lastUsed: '2024-01-15T11:20:00Z',
    capabilities: ['Task Management', 'Workflow Coordination', 'Progress Tracking'],
  },
]

export function Agents() {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')

  const filteredAgents = agents.filter(agent => {
    const matchesSearch = agent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         agent.role.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' || agent.status === filterStatus
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Agents</h1>
          <p className="text-gray-600">Manage your AI agents and their configurations</p>
        </div>
        <Button className="btn-primary">
          <Plus className="mr-2 h-4 w-4" />
          Create Agent
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
                  placeholder="Search agents..."
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
                variant={filterStatus === 'active' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('active')}
              >
                Active
              </Button>
              <Button
                variant={filterStatus === 'inactive' ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('inactive')}
              >
                Inactive
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredAgents.map((agent) => (
          <Card key={agent.id} className="hover:shadow-md transition-shadow">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div>
                  <CardTitle className="text-lg">{agent.name}</CardTitle>
                  <p className="text-sm text-gray-600 mt-1">{agent.role}</p>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge
                    variant={agent.status === 'active' ? 'success' : 'secondary'}
                  >
                    {agent.status}
                  </Badge>
                  <Button variant="ghost" size="sm">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <p className="text-sm text-gray-700 line-clamp-2">
                  {agent.goal}
                </p>
                
                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Model:</span>
                    <span className="font-medium">{agent.model}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Executions:</span>
                    <span className="font-medium">{agent.executions}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Success Rate:</span>
                    <span className="font-medium text-success-600">
                      {agent.successRate}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-500">Last Used:</span>
                    <span className="font-medium">
                      {formatRelativeTime(agent.lastUsed)}
                    </span>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-sm font-medium text-gray-700">Capabilities:</p>
                  <div className="flex flex-wrap gap-1">
                    {agent.capabilities.map((capability) => (
                      <Badge key={capability} variant="outline" size="sm">
                        {capability}
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="flex space-x-2 pt-4">
                  <Button variant="outline" size="sm" className="flex-1">
                    <Play className="mr-2 h-4 w-4" />
                    Test
                  </Button>
                  <Button variant="outline" size="sm" className="flex-1">
                    <Edit className="mr-2 h-4 w-4" />
                    Edit
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
      {filteredAgents.length === 0 && (
        <Card>
          <CardContent className="p-12 text-center">
            <div className="mx-auto max-w-md">
              <div className="mx-auto h-12 w-12 text-gray-400">
                <Search className="h-12 w-12" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900">
                No agents found
              </h3>
              <p className="mt-2 text-sm text-gray-500">
                {searchTerm || filterStatus !== 'all'
                  ? 'Try adjusting your search or filter criteria.'
                  : 'Get started by creating your first agent.'}
              </p>
              {!searchTerm && filterStatus === 'all' && (
                <div className="mt-6">
                  <Button className="btn-primary">
                    <Plus className="mr-2 h-4 w-4" />
                    Create Agent
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