"use client"

import type React from "react"

import { useState } from "react"
import Link from "next/link"

interface Message {
  id: string
  type: "user" | "agent"
  content: string
  timestamp: Date
}

export default function DashboardAgentPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const formatResponse = (text: string) => {
    // Convert **text** to bold
    return text.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      // Replace with your actual API endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/dashboard-agent/prompt`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt: input }),
      })

      const data = await response.json()

      if (data.success) {
        const agentMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: "agent",
          content: data.response,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, agentMessage])
      }
    } catch (error) {
      // Mock response for demo
      console.log("error" , error);
      const mockResponse: Message = {
        id: (Date.now() + 1).toString(),
        type: "agent",
        content:
          "**Dashboard Overview:**\n- **Total Users:** 1,247\n- **Active Sessions:** 89\n- **Revenue This Month:** $45,230\n- **Course Completion Rate:** 78%\n- **Top Performing Course:** Advanced JavaScript\n- **Support Tickets:** 12 pending",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, mockResponse])
    } finally {
      setIsLoading(false)
    }
  }

  const quickActions = [
    { label: "Give the most enrolled classes", icon: "📊" },
    { label: "Return Total Revenue", icon: "💰" },
    { label: "What are the course completion rates", icon: "📚" },
    { label: "Are there any client birthday reminders", icon: "🎯" },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link href="/" className="flex items-center text-gray-600 hover:text-gray-900 transition-colors">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                Back to Home
              </Link>
            </div>
            <h1 className="text-xl font-semibold text-gray-900">Dashboard Agent</h1>
            <div className="w-24"></div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto p-4 h-[calc(100vh-4rem)] flex gap-6">
        {/* Quick Actions Sidebar */}
        <div className="w-80 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={() => setInput(action.label)}
                className="w-full text-left p-3 rounded-lg border border-gray-200 hover:border-purple-300 hover:bg-purple-50 transition-all group"
              >
                <div className="flex items-center space-x-3">
                  <span className="text-xl">{action.icon}</span>
                  <span className="text-gray-700 group-hover:text-purple-700">{action.label}</span>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-8 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border border-purple-100">
            <h3 className="font-medium text-gray-900 mb-2">💡 Pro Tip</h3>
            <p className="text-sm text-gray-600">
              Ask specific questions about metrics, user behavior, or performance data to get detailed insights.
            </p>
          </div>
        </div>

        {/* Chat Container */}
        <div className="flex-1 flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto mb-4 space-y-4">
            {messages.length === 0 ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Welcome to Dashboard Agent</h3>
                <p className="text-gray-600">Get insights about analytics, performance metrics, and business data.</p>
              </div>
            ) : (
              messages.map((message) => (
                <div key={message.id} className={`flex ${message.type === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-xs lg:max-w-2xl px-4 py-3 rounded-2xl ${
                      message.type === "user"
                        ? "bg-purple-600 text-white"
                        : "bg-white text-gray-900 shadow-sm border border-gray-200"
                    }`}
                  >
                    {message.type === "agent" ? (
                      <div
                        className="whitespace-pre-line"
                        dangerouslySetInnerHTML={{
                          __html: formatResponse(message.content),
                        }}
                      />
                    ) : (
                      <p className="whitespace-pre-line">{message.content}</p>
                    )}
                    <p className={`text-xs mt-2 ${message.type === "user" ? "text-purple-100" : "text-gray-500"}`}>
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))
            )}

            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-900 shadow-sm border border-gray-200 max-w-xs lg:max-w-md px-4 py-3 rounded-2xl">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.1s" }}
                      ></div>
                      <div
                        className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                        style={{ animationDelay: "0.2s" }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-500">Analyzing data...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="flex space-x-4">
            <div className="flex-1">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about analytics, metrics, or performance data..."
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent outline-none transition-all"
                disabled={isLoading}
              />
            </div>
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-6 py-3 bg-purple-600 text-white rounded-xl hover:bg-purple-700 focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                />
              </svg>
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
