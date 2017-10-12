# frozen_string_literal: true

class JobsController < ApplicationController
  before_action :set_job, only: %i(show edit update destroy)

  # GET /jobs
  # GET /jobs.json
  def index
    @jobs = Job.all
  end

  # GET /jobs/1
  # GET /jobs/1.json
  def show
  end

  # GET /jobs/new
  def new
    @job = Job.new
  end

  # GET /jobs/1/edit
  def edit
  end

  # POST /jobs
  # POST /jobs.json
  def create
    @job = Job.new(job_params.merge(worker: find_free_worker, status: "DISPATCHED"))

    respond_to do |format|
      if @job.save
        @job.worker.channel.trigger(:spawn, @job.request_json, namespace: :worker)

        format.html { redirect_to @job, notice: "Job was successfully created." }
        format.json { render :show, status: :created, location: @job }
      else
        format.html { render :new }
        format.json { render json: @job.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /jobs/1
  # PATCH/PUT /jobs/1.json
  def update
    respond_to do |format|
      if @job.update(job_params)
        format.html { redirect_to @job, notice: "Job was successfully updated." }
        format.json { render :show, status: :ok, location: @job }
      else
        format.html { render :edit }
        format.json { render json: @job.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /jobs/1
  # DELETE /jobs/1.json
  def destroy
    @job.destroy
    respond_to do |format|
      format.html { redirect_to jobs_url, notice: "Job was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  def set_job
    @job = Job.find(params[:id])
  end

  def find_free_worker
    current_user
      .workers
      .joins("left outer join jobs on jobs.worker_id = workers.id")
      .group("workers.id")
      .order("count(distinct jobs.id) asc")
      .first
  end

  def job_params
    params
      .require(:job)
      .permit(:job_type_id)
  end
end
