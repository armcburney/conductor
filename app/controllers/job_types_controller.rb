# frozen_string_literal: true

class JobTypesController < ApplicationController
  before_action :set_job_type, only: %i(show edit update destroy)

  # GET /job_types
  # GET /job_types.json
  def index
    @job_types = JobType.all
  end

  # GET /job_types/1
  # GET /job_types/1.json
  def show
  end

  # GET /job_types/new
  def new
    @job_type = JobType.new
  end

  # GET /job_types/1/edit
  def edit
  end

  # POST /job_types
  # POST /job_types.json
  def create
    @job_type = JobType.new(job_type_params)

    respond_to do |format|
      if @job_type.save
        format.html { redirect_to @job_type, notice: "Job type was successfully created." }
        format.json { render :show, status: :created, location: @job_type }
      else
        format.html { render :new }
        format.json { render json: @job_type.errors, status: :unprocessable_entity }
      end
    end
  end

  # PATCH/PUT /job_types/1
  # PATCH/PUT /job_types/1.json
  def update
    respond_to do |format|
      if @job_type.update(job_type_params)
        format.html { redirect_to @job_type, notice: "Job type was successfully updated." }
        format.json { render :show, status: :ok, location: @job_type }
      else
        format.html { render :edit }
        format.json { render json: @job_type.errors, status: :unprocessable_entity }
      end
    end
  end

  # DELETE /job_types/1
  # DELETE /job_types/1.json
  def destroy
    @job_type.destroy
    respond_to do |format|
      format.html { redirect_to job_types_url, notice: "Job type was successfully destroyed." }
      format.json { head :no_content }
    end
  end

  private

  def set_job_type
    @job_type = JobType.find(params[:id])
  end

  def job_type_params
    params
      .require(:job_type)
      .permit(:script, :working_directory, :environment_variables, :timeout, :name, :user_id)
  end
end
