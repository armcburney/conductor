class WorkerConnectionController < WebsocketRails::BaseController

  #def initialize_session
  #end

  #def authorize_public
    #WebsocketRails[message['channel']].make_private
  #end

  def connect
    if worker
      trigger_success
    else
      trigger_failure
    end
  end

  private

  def worker_user
    @worker_user ||= User.joins(:api_keys).where(api_keys: {key: message["key"]}).first
  end

  def worker
    @worker ||= Worker.find_by(address: message["address"])

    # Create if it doesn't exist
    @worker ||= worker_user.workers.create(address: message["address"])
  end
end
