import React, { useState } from 'react';
import { Users, UserCheck, UserX, Clock, Filter } from 'lucide-react';

function Dashboard() {
  const [selectedCourse, setSelectedCourse] = useState('all');
  const [selectedSection, setSelectedSection] = useState('all');

  const stats = [
    { title: 'Total Students', value: '2,547', icon: Users, color: 'bg-blue-500' },
    { title: 'Present Today', value: '1,923', icon: UserCheck, color: 'bg-green-500' },
    { title: 'Absent Today', value: '624', icon: UserX, color: 'bg-red-500' },
    { title: 'Average Attendance', value: '89%', icon: Clock, color: 'bg-purple-500' },
  ];

  const recentActivity = [
    { name: 'Khushi Diwan', time: '2 minutes ago', status: 'Present', course: 'B.Tech', section: 'A' },
    { name: 'Devansh Datta', time: '5 minutes ago', status: 'Present', course: 'B.Tech', section: 'A' },
    { name: 'Pooja Batra', time: '10 minutes ago', status: 'Present', course: 'B.Tech', section: 'A' },
    { name: 'Aarti Chugh', time: '15 minutes ago', status: 'Present', course: 'B.Tech', section: 'A' },
  ];

  const filteredActivity = recentActivity.filter(activity => 
    (selectedCourse === 'all' || activity.course === selectedCourse) &&
    (selectedSection === 'all' || activity.section === selectedSection)
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <div key={index} className="bg-[#1e2533] rounded-lg overflow-hidden shadow-lg">
            <div className="p-4 flex items-center">
              <div className={`p-3 rounded-lg ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <div className="ml-4">
                <h3 className="text-gray-400 text-sm">{stat.title}</h3>
                <p className="text-white text-2xl font-semibold">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="mt-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-white text-lg">Recent Activity</h2>
          
          {/* Filters - keeping them subtle and aligned with your dark theme */}
          <div className="flex gap-4">
            <select
              value={selectedCourse}
              onChange={(e) => setSelectedCourse(e.target.value)}
              className="bg-[#1e2533] text-gray-300 text-sm rounded-md border border-gray-700 px-3 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="all">All Courses</option>
              <option value="B.Tech">B.Tech</option>
              <option value="MBA">MBA</option>
              <option value="BCA">BCA</option>
            </select>
            
            <select
              value={selectedSection}
              onChange={(e) => setSelectedSection(e.target.value)}
              className="bg-[#1e2533] text-gray-300 text-sm rounded-md border border-gray-700 px-3 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
              <option value="all">All Sections</option>
              <option value="A">Section A</option>
              <option value="B">Section B</option>
              <option value="C">Section C</option>
            </select>
          </div>
        </div>

        <div className="bg-[#1e2533] rounded-lg shadow-lg">
          {filteredActivity.map((activity, index) => (
            <div key={index} className="border-b border-gray-700 last:border-b-0">
              <div className="px-4 py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-blue-400">{activity.name}</span>
                    <span className="text-gray-500 text-sm">{activity.course} - Section {activity.section}</span>
                  </div>
                  <span className="px-2 py-1 text-xs rounded-full bg-green-500 text-white">
                    {activity.status}
                  </span>
                </div>
                <div className="mt-2 flex items-center text-gray-400">
                  <Clock className="w-4 h-4 mr-2" />
                  <span className="text-sm">{activity.time}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;