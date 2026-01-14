"""
Simple GSM API for Testing

Basic Flask API for GSM communication testing without complex dependencies.
Provides mock endpoints for SMS, calls, and emergency features.
"""

from flask import Flask, jsonify, request
from datetime import datetime
import random

app = Flask(__name__)

# Mock data storage
gsm_messages = []
gsm_calls = []
gsm_system_status = {
    'system_active': True,
    'sim_card_number': '+1234567890',
    'emergency_mode': False,
    'auto_answer_enabled': True,
    'guardian_contacts': [
        {'id': 'guardian_001', 'name': 'John Guardian', 'phone': '+1234567890'},
        {'id': 'guardian_002', 'name': 'Jane Guardian', 'phone': '+0987654321'}
    ],
    'emergency_contacts': ['+911', '+112'],
    'outgoing_messages': 0,
    'incoming_messages': 0,
    'missed_calls': 0,
    'call_history': 0
}

@app.route('/api/gsm/status', methods=['GET'])
def gsm_status():
    """Get GSM system status."""
    return jsonify({
        'success': True,
        'status': gsm_system_status,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/sms/send', methods=['POST'])
def send_sms():
    """Send SMS message."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['guardian_id', 'message']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    guardian_id = data['guardian_id']
    message = data['message']
    priority = data.get('priority', 'normal')
    
    # Create message record
    sms_message = {
        'id': len(gsm_messages) + 1,
        'type': 'outgoing',
        'guardian_id': guardian_id,
        'message': message,
        'priority': priority,
        'timestamp': datetime.now().isoformat(),
        'delivered': True,
        'status': 'sent'
    }
    
    gsm_messages.append(sms_message)
    gsm_system_status['outgoing_messages'] += 1
    
    return jsonify({
        'success': True,
        'message': 'SMS sent successfully',
        'guardian_id': guardian_id,
        'message_preview': message[:50] + '...' if len(message) > 50 else message,
        'priority': priority,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/call/initiate', methods=['POST'])
def initiate_call():
    """Initiate voice call."""
    data = request.get_json()
    
    # Validate required fields
    if 'guardian_id' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required field: guardian_id'
        }), 400
    
    guardian_id = data['guardian_id']
    priority = data.get('priority', 'normal')
    
    # Create call record
    voice_call = {
        'id': len(gsm_calls) + 1,
        'type': 'outgoing',
        'guardian_id': guardian_id,
        'priority': priority,
        'timestamp': datetime.now().isoformat(),
        'duration': random.randint(10, 300),
        'answered': random.choice([True, False]),
        'connected': random.choice([True, False]),
        'status': 'completed'
    }
    
    gsm_calls.append(voice_call)
    gsm_system_status['call_history'] += 1
    
    return jsonify({
        'success': True,
        'message': 'Voice call initiated',
        'guardian_id': guardian_id,
        'priority': priority,
        'call_id': voice_call['id'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/emergency', methods=['POST'])
def emergency_alert():
    """Send emergency alert."""
    data = request.get_json()
    
    # Validate required fields
    if 'alert_type' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required field: alert_type'
        }), 400
    
    alert_type = data['alert_type']
    location = data.get('location', {})
    medical_info = data.get('medical_info', {})
    
    # Create emergency alert
    emergency_message = {
        'id': len(gsm_messages) + 1,
        'type': 'emergency',
        'alert_type': alert_type,
        'location': location,
        'medical_info': medical_info,
        'timestamp': datetime.now().isoformat(),
        'delivered': True,
        'status': 'emergency_sent'
    }
    
    gsm_messages.append(emergency_message)
    gsm_system_status['emergency_mode'] = True
    gsm_system_status['outgoing_messages'] += 1
    
    # Simulate sending to all contacts
    for guardian in gsm_system_status['guardian_contacts']:
        guardian_message = {
            'id': len(gsm_messages) + 1,
            'type': 'emergency_notification',
            'guardian_id': guardian['id'],
            'message': f"🚨 EMERGENCY: {alert_type}",
            'timestamp': datetime.now().isoformat(),
            'delivered': True,
            'status': 'delivered'
        }
        gsm_messages.append(guardian_message)
    
    return jsonify({
        'success': True,
        'message': 'Emergency alert sent',
        'alert_type': alert_type,
        'location': location,
        'medical_info': medical_info,
        'notified_contacts': len(gsm_system_status['guardian_contacts']),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/commands', methods=['GET'])
def get_commands():
    """Get available SMS commands."""
    commands = {
        'STATUS': {
            'description': 'Get current device status',
            'usage': 'STATUS',
            'example': 'STATUS'
        },
        'LOCATION': {
            'description': 'Get current location',
            'usage': 'LOCATION',
            'example': 'LOCATION'
        },
        'HEALTH': {
            'description': 'Get health status',
            'usage': 'HEALTH',
            'example': 'HEALTH'
        },
        'CALL': {
            'description': 'Make voice call',
            'usage': 'CALL <phone_number>',
            'example': 'CALL +1234567890'
        },
        'ALERT': {
            'description': 'Send alert to guardians',
            'usage': 'ALERT <message>',
            'example': 'ALERT I need help immediately'
        },
        'HELP': {
            'description': 'Show available commands',
            'usage': 'HELP',
            'example': 'HELP'
        },
        'BATTERY': {
            'description': 'Get battery level',
            'usage': 'BATTERY',
            'example': 'BATTERY'
        },
        'SILENCE': {
            'description': 'Silence non-emergency alerts',
            'usage': 'SILENCE',
            'example': 'SILENCE'
        },
        'TEST': {
            'description': 'Test system functionality',
            'usage': 'TEST',
            'example': 'TEST'
        }
    }
    
    return jsonify({
        'success': True,
        'commands': commands,
        'total_commands': len(commands),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/messages', methods=['GET'])
def get_messages():
    """Get message history."""
    message_type = request.args.get('type', 'all')
    limit = int(request.args.get('limit', 50))
    
    # Filter messages
    if message_type == 'incoming':
        filtered_messages = [msg for msg in gsm_messages if msg.get('type') == 'incoming']
    elif message_type == 'outgoing':
        filtered_messages = [msg for msg in gsm_messages if msg.get('type') == 'outgoing']
    elif message_type == 'emergency':
        filtered_messages = [msg for msg in gsm_messages if msg.get('type') == 'emergency']
    else:
        filtered_messages = gsm_messages
    
    # Return limited results
    messages = filtered_messages[-limit:]
    
    return jsonify({
        'success': True,
        'messages': messages,
        'message_type': message_type,
        'total_messages': len(messages),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/calls', methods=['GET'])
def get_calls():
    """Get call history."""
    limit = int(request.args.get('limit', 50))
    
    # Return limited results
    calls = gsm_calls[-limit:]
    
    return jsonify({
        'success': True,
        'calls': calls,
        'total_calls': len(calls),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/contacts/guardians', methods=['GET'])
def get_guardian_contacts():
    """Get guardian contact list."""
    return jsonify({
        'success': True,
        'guardians': gsm_system_status['guardian_contacts'],
        'total_guardians': len(gsm_system_status['guardian_contacts']),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/gsm/test', methods=['POST'])
def test_gsm():
    """Test GSM system functionality."""
    data = request.get_json()
    test_type = data.get('test_type', 'sms')
    guardian_id = data.get('guardian_id', 'test_guardian')
    
    result = {'success': False, 'message': ''}
    
    if test_type == 'sms':
        # Simulate SMS test
        test_message = {
            'id': len(gsm_messages) + 1,
            'type': 'test',
            'guardian_id': guardian_id,
            'message': '🧪 GSM Test Message - System is working correctly!',
            'timestamp': datetime.now().isoformat(),
            'delivered': True,
            'status': 'test_completed'
        }
        gsm_messages.append(test_message)
        result = {
            'success': True,
            'message': 'SMS test completed',
            'test_id': test_message['id']
        }
    
    elif test_type == 'call':
        # Simulate call test
        test_call = {
            'id': len(gsm_calls) + 1,
            'type': 'test',
            'guardian_id': guardian_id,
            'timestamp': datetime.now().isoformat(),
            'duration': 5,
            'answered': True,
            'connected': True,
            'status': 'test_completed'
        }
        gsm_calls.append(test_call)
        result = {
            'success': True,
            'message': 'Call test completed',
            'test_id': test_call['id']
        }
    
    elif test_type == 'emergency':
        # Simulate emergency test
        emergency_test = {
            'id': len(gsm_messages) + 1,
            'type': 'emergency_test',
            'guardian_id': guardian_id,
            'message': '🧪 Emergency Test - System emergency response working!',
            'timestamp': datetime.now().isoformat(),
            'delivered': True,
            'status': 'emergency_test_completed'
        }
        gsm_messages.append(emergency_test)
        result = {
            'success': True,
            'message': 'Emergency test completed',
            'test_id': emergency_test['id']
        }
    
    else:
        result = {
            'success': False,
            'message': f'Unknown test type: {test_type}'
        }
    
    return jsonify({
        'success': result['success'],
        'message': result['message'],
        'test_type': test_type,
        'guardian_id': guardian_id,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("📱 Starting Simple GSM API for Testing...")
    print("📡 Available on: http://localhost:5002")
    print("🔍 GSM status: http://localhost:5002/api/gsm/status")
    print("📨 Send SMS: http://localhost:5002/api/gsm/sms/send")
    print("📞 Initiate call: http://localhost:5002/api/gsm/call/initiate")
    print("🚨 Emergency alert: http://localhost:5002/api/gsm/emergency")
    print("📋 Commands: http://localhost:5002/api/gsm/commands")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5002, debug=True)
