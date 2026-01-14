"""
GSM Communication API Endpoints

Provides REST API endpoints for two-way GSM communication between guardians and seniors.
Supports SMS messaging, voice calls, emergency alerts, and remote commands.

Endpoints:
- /api/gsm/sms/send - Send SMS message
- /api/gsm/call/initiate - Initiate voice call
- /api/gsm/emergency - Send emergency alert
- /api/gsm/commands - Process SMS commands
- /api/gsm/status - Get GSM system status
"""

from flask import Flask, request, jsonify
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.communication.enhanced_gsm_system import (
    get_gsm_system, send_guardian_sms, initiate_guardian_call, 
    send_emergency_alert, CallPriority
)

app = Flask(__name__)

@app.route('/api/gsm/sms/send', methods=['POST'])
def send_sms_endpoint():
    """Send SMS message from guardian to senior."""
    try:
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
        
        # Convert priority string to enum
        priority_map = {
            'low': CallPriority.LOW,
            'normal': CallPriority.NORMAL,
            'high': CallPriority.HIGH,
            'emergency': CallPriority.EMERGENCY
        }
        call_priority = priority_map.get(priority, CallPriority.NORMAL)
        
        # Import here to avoid circular imports
        import asyncio
        from src.communication.enhanced_gsm_system import get_gsm_system
        
        # Get GSM system and send SMS
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(gsm_system.send_guardian_sms(guardian_id, message, call_priority))
        finally:
            loop.close()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'SMS sent successfully',
                'guardian_id': guardian_id,
                'message_preview': message[:50] + '...' if len(message) > 50 else message,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send SMS'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/call/initiate', methods=['POST'])
def initiate_call_endpoint():
    """Initiate voice call from guardian to senior."""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'guardian_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: guardian_id'
            }), 400
        
        guardian_id = data['guardian_id']
        priority = data.get('priority', 'normal')
        
        # Convert priority string to enum
        priority_map = {
            'low': CallPriority.LOW,
            'normal': CallPriority.NORMAL,
            'high': CallPriority.HIGH,
            'emergency': CallPriority.EMERGENCY
        }
        call_priority = priority_map.get(priority, CallPriority.NORMAL)
        
        # Import here to avoid circular imports
        import asyncio
        from src.communication.enhanced_gsm_system import get_gsm_system
        
        # Get GSM system and initiate call
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(gsm_system.initiate_voice_call(guardian_id, call_priority))
        finally:
            loop.close()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Voice call initiated',
                'guardian_id': guardian_id,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to initiate voice call'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/emergency', methods=['POST'])
def emergency_alert_endpoint():
    """Send emergency alert via GSM."""
    try:
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
        
        # Import here to avoid circular imports
        import asyncio
        from src.communication.enhanced_gsm_system import get_gsm_system
        
        # Get GSM system and send emergency alert
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            success = loop.run_until_complete(gsm_system.send_emergency_alert(alert_type, location, medical_info))
        finally:
            loop.close()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Emergency alert sent',
                'alert_type': alert_type,
                'location': location,
                'medical_info': medical_info,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send emergency alert'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/commands', methods=['GET'])
def get_commands_endpoint():
    """Get available SMS commands."""
    try:
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/status', methods=['GET'])
def get_gsm_status_endpoint():
    """Get GSM system status."""
    try:
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        status = {
            'system_active': True,
            'sim_card_number': gsm_system.sim_card_number,
            'emergency_mode': gsm_system.emergency_mode,
            'auto_answer_enabled': gsm_system.auto_answer_enabled,
            'guardian_contacts': len(gsm_system.guardian_contacts),
            'emergency_contacts': len(gsm_system.emergency_contacts),
            'outgoing_messages': len(gsm_system.outgoing_messages),
            'incoming_messages': len(gsm_system.incoming_messages),
            'missed_calls': len(gsm_system.missed_calls),
            'call_history': len(gsm_system.call_history),
            'available_commands': list(gsm_system.sms_commands.keys()),
            'rate_limits': {
                'sms_rate_limit': gsm_system.sms_rate_limit,
                'call_rate_limit': gsm_system.call_rate_limit
            }
        }
        
        return jsonify({
            'success': True,
            'status': status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/messages', methods=['GET'])
def get_messages_endpoint():
    """Get message history."""
    try:
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        # Get message type filter
        message_type = request.args.get('type', 'all')
        limit = int(request.args.get('limit', 50))
        
        # Filter messages
        if message_type == 'incoming':
            messages = gsm_system.incoming_messages[-limit:]
        elif message_type == 'outgoing':
            messages = gsm_system.outgoing_messages[-limit:]
        else:
            # Combine all messages
            all_messages = []
            for msg in gsm_system.incoming_messages:
                all_messages.append({
                    'id': msg.message_id,
                    'type': 'incoming',
                    'sender': msg.sender,
                    'recipient': msg.recipient,
                    'content': msg.content,
                    'timestamp': msg.timestamp,
                    'priority': msg.priority.value
                })
            for msg in gsm_system.outgoing_messages:
                all_messages.append({
                    'id': msg.message_id,
                    'type': 'outgoing',
                    'sender': msg.sender,
                    'recipient': msg.recipient,
                    'content': msg.content,
                    'timestamp': msg.timestamp,
                    'priority': msg.priority.value
                })
            
            # Sort by timestamp
            messages = sorted(all_messages, key=lambda x: x['timestamp'], reverse=True)[:limit]
        
        return jsonify({
            'success': True,
            'messages': messages,
            'message_type': message_type,
            'total_messages': len(messages),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/calls', methods=['GET'])
def get_calls_endpoint():
    """Get call history."""
    try:
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        limit = int(request.args.get('limit', 50))
        
        # Get call history
        calls = []
        for call in gsm_system.call_history[-limit:]:
            calls.append({
                'id': call.call_id,
                'caller': call.caller,
                'recipient': call.recipient,
                'timestamp': call.timestamp,
                'duration': call.duration,
                'priority': call.priority.value,
                'answered': call.answered,
                'connected': call.connected
            })
        
        # Add missed calls
        for call in gsm_system.missed_calls[-limit:]:
            calls.append({
                'id': call.call_id,
                'caller': call.caller,
                'recipient': call.recipient,
                'timestamp': call.timestamp,
                'duration': 0,
                'priority': call.priority.value,
                'answered': False,
                'connected': False,
                'missed': True
            })
        
        # Sort by timestamp
        calls = sorted(calls, key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'success': True,
            'calls': calls,
            'total_calls': len(calls),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/contacts/guardians', methods=['GET'])
def get_guardian_contacts_endpoint():
    """Get guardian contact list."""
    try:
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        return jsonify({
            'success': True,
            'guardians': gsm_system.guardian_contacts,
            'total_guardians': len(gsm_system.guardian_contacts),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/gsm/test', methods=['POST'])
def test_gsm_endpoint():
    """Test GSM system functionality."""
    try:
        data = request.get_json()
        test_type = data.get('test_type', 'sms')
        guardian_id = data.get('guardian_id', 'test_guardian')
        
        gsm_system = get_gsm_system()
        if not gsm_system:
            return jsonify({
                'success': False,
                'error': 'GSM system not initialized'
            }), 500
        
        result = {'success': False, 'message': ''}
        
        if test_type == 'sms':
            success = await send_guardian_sms(
                guardian_id, 
                "🧪 GSM Test Message - System is working correctly!",
                CallPriority.NORMAL
            )
            result = {
                'success': success,
                'message': 'SMS test completed' if success else 'SMS test failed'
            }
        
        elif test_type == 'call':
            success = await initiate_guardian_call(guardian_id, CallPriority.NORMAL)
            result = {
                'success': success,
                'message': 'Call test completed' if success else 'Call test failed'
            }
        
        elif test_type == 'emergency':
            success = await send_emergency_alert(
                "Test Emergency Alert",
                {"test": True, "location": "Test Location"},
                {"test": True, "conditions": ["None"]}
            )
            result = {
                'success': success,
                'message': 'Emergency test completed' if success else 'Emergency test failed'
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
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("📱 Starting GSM Communication API...")
    app.run(host='0.0.0.0', port=5002, debug=True)
